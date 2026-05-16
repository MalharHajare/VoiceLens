from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import librosa
import numpy as np
import requests
import tempfile
import os
import re
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variables for lazy model loading
whisper_model = None
model_loading = False
model_load_error = None
model_lock = threading.Lock()

FILLERS = ["um","uh","like","you know","kind of","basically","so","right",
           "actually","literally","i mean","you see","sort of"]
IDEAL_MIN, IDEAL_MAX = 120, 160


def load_whisper_model():
    """Load Whisper model in a thread-safe way"""
    global whisper_model, model_loading, model_load_error
    
    with model_lock:
        if whisper_model is not None:
            return whisper_model
        
        if model_loading:
            # Wait for another thread to finish loading
            while model_loading:
                time.sleep(0.1)
            return whisper_model
        
        model_loading = True
    
    try:
        print("Loading Whisper model (this may take 10-30 seconds)...")
        start_time = time.time()
        model = whisper.load_model("base")
        load_time = time.time() - start_time
        print(f"✓ Whisper model loaded successfully in {load_time:.1f} seconds")
        
        with model_lock:
            whisper_model = model
            model_loading = False
        return model
    except Exception as e:
        print(f"✗ Failed to load Whisper model: {e}")
        with model_lock:
            model_load_error = str(e)
            model_loading = False
        raise


@app.route("/", methods=["GET"])
def index():
    status = "ready" if whisper_model else "loading" if model_loading else "not_loaded"
    return jsonify({
        "status": "VoiceLens backend running",
        "model_status": status,
        "error": model_load_error
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "healthy": True,
        "model_loaded": whisper_model is not None,
        "model_loading": model_loading,
        "model_error": model_load_error
    })


@app.route("/analyse", methods=["POST"])
def analyse():
    # Ensure model is loaded
    try:
        model = load_whisper_model()
    except Exception as e:
        return jsonify({"error": f"Model loading failed: {str(e)}"}), 500
    
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    hf_token = request.form.get("hf_token", "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        transcript, duration = transcribe(tmp_path, model)
        af = audio_features(tmp_path, duration)
        ta = text_analysis(transcript, duration, af)
        sentiment = hf_sentiment(transcript, hf_token) if hf_token else None
        return jsonify(build_result(transcript, ta, af, sentiment, duration))
    except Exception as e:
        print(f"Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


def transcribe(path, model):
    result = model.transcribe(path, language="en")
    text = result["text"].strip()
    dur = result["segments"][-1]["end"] if result["segments"] else 30
    return text, dur


def audio_features(path, duration):
    try:
        y, sr = librosa.load(path, sr=16000, duration=120)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pv = pitches[magnitudes > np.percentile(magnitudes, 75)]
        avg_pitch = float(np.mean(pv[pv > 0])) if len(pv[pv > 0]) > 0 else 0
        rms = librosa.feature.rms(y=y)[0]
        e_mean = float(np.mean(rms))
        e_std = float(np.std(rms))
        sil_ratio = float(np.sum(rms < e_mean * 0.1) / len(rms))
        return {"avg_pitch": avg_pitch, "energy_mean": e_mean,
                "energy_std": e_std, "silence_ratio": sil_ratio, "duration": duration}
    except Exception as e:
        print(f"Audio features error: {e}")
        return {"avg_pitch": 0, "energy_mean": 0, "energy_std": 0,
                "silence_ratio": 0.1, "duration": duration}


def text_analysis(transcript, duration, af):
    lower = transcript.lower()
    words = [w for w in re.split(r'\s+', transcript.strip()) if w]
    wc = len(words)
    filler_count = 0
    found = []
    for f in FILLERS:
        m = re.findall(r'\b' + re.escape(f) + r'\b', lower)
        if m:
            filler_count += len(m)
            found.append(f)

    wpm = round((wc / duration) * 60) if duration > 0 else 130
    fr = filler_count / max(wc, 1)
    fluency = max(15, round(100 - fr * 300))

    if IDEAL_MIN <= wpm <= IDEAL_MAX:
        pace = min(98, round(88 + (1 - abs(wpm - 140) / 20) * 10))
    elif wpm < IDEAL_MIN:
        pace = max(30, round(88 - (IDEAL_MIN - wpm) * 0.8))
    else:
        pace = max(30, round(88 - (wpm - IDEAL_MAX) * 0.6))

    sents = [s for s in re.split(r'[.!?]+', transcript) if len(s.strip()) > 3]
    avg_sl = wc / max(len(sents), 1)
    clarity = round(max(40, min(95, 65 + (15 if avg_sl > 8 else 0) - fr * 120)))
    e_factor = min(20, af["energy_std"] * 200)
    confidence = round(fluency * 0.45 + pace * 0.3 + clarity * 0.15 + e_factor * 0.1)

    patterns = []
    if fr > 0.08:
        patterns.append({"label":"High filler word use","severity":"high","description":f"{filler_count} fillers in {wc} words ({round(fr*100)}%) — ideal is under 3%."})
    elif fr > 0.03:
        patterns.append({"label":"Moderate filler words","severity":"mid","description":f"{filler_count} fillers — you're close to the ideal range."})
    else:
        patterns.append({"label":"Low filler word use","severity":"low","description":f"Only {filler_count} fillers — excellent control."})

    if wpm < 100:
        patterns.append({"label":"Pace too slow","severity":"mid","description":f"{wpm} wpm is below the ideal 120-160 wpm range."})
    elif wpm > 180:
        patterns.append({"label":"Pace too fast","severity":"mid","description":f"{wpm} wpm may feel rushed — slow down slightly."})
    else:
        patterns.append({"label":"Good speaking pace","severity":"low","description":f"{wpm} wpm is in the natural comfortable range."})

    pp = round(af["silence_ratio"] * 100)
    if af["silence_ratio"] > 0.4:
        patterns.append({"label":"Excessive pausing","severity":"mid","description":f"{pp}% silence — try to maintain a steadier flow."})
    elif af["silence_ratio"] < 0.05:
        patterns.append({"label":"Too little pausing","severity":"mid","description":"Very few pauses — deliberate pauses improve comprehension."})
    else:
        patterns.append({"label":"Good pause rhythm","severity":"low","description":f"{pp}% pause ratio — a natural rhythm."})

    therapy = fr > 0.12 or wpm > 200 or (wpm < 80 and duration > 20)
    therapy_reason = (
        "The frequency of disfluencies suggests a speech-language pathologist could provide targeted structured help."
        if therapy else
        "Your speech is progressing well — self-practice with these exercises should yield strong improvement."
    )

    ai = build_ai_text(fluency, pace, clarity, filler_count, wpm, wc, found, af)
    exercises = build_exercises(found, wpm, fluency)

    return {"word_count":wc,"wpm":wpm,"filler_count":filler_count,"filler_words":found,
            "scores":{"fluency":fluency,"clarity":clarity,"pace":pace,"confidence":confidence},
            "patterns":patterns,"therapy_recommended":therapy,"therapy_reason":therapy_reason,
            "ai_analysis":ai,"exercises":exercises}


def build_ai_text(fluency, pace, clarity, fc, wpm, wc, fillers, af):
    s = ("Your speech demonstrates <strong>strong natural fluency</strong> with a good command of language structure."
         if fluency > 70 else
         "Your speech shows <strong>solid foundational skills</strong> — with practice these will grow significantly."
         if fluency > 50 else
         "Your speech has the building blocks of clear communication — <strong>the habits holding you back are trainable</strong>.")
    f = ("<strong>No filler words detected</strong> — impressive preparation." if fc == 0 else
         f"Only <strong>{fc} filler word{'s' if fc>1 else ''}</strong> — you're above average." if fc <= 3 else
         f"You used <strong>{fc} filler words</strong> ({', '.join(fillers[:3])}). Filler reduction is one of the fastest speech skills to improve with daily practice.")
    p = (f"Your pace of <strong>{wpm} wpm</strong> is ideal — comfortable for listeners." if 120<=wpm<=160 else
         f"At <strong>{wpm} wpm</strong>, your pace is a little slow. A slight increase will sound more energetic." if wpm<120 else
         f"At <strong>{wpm} wpm</strong>, you're speaking fast. Deliberate pauses will help listeners keep up.")
    e = ("\n\nYour <strong>vocal energy variation is strong</strong> — you naturally emphasise key words which keeps listeners engaged."
         if af["energy_std"] > 0.02 else
         "\n\nYour voice has a <strong>fairly flat energy pattern</strong>. Try emphasising key words — it keeps listeners engaged.")
    return f"{s}\n\n{f}\n\n{p}{e}"


def build_exercises(fillers, wpm, fluency):
    ex = []
    if fillers:
        ex.append({"title":"Silent pause drill","description":f"Record yourself for 60 seconds. Every time you feel the urge to say '{fillers[0]}', pause silently instead. Count improvements each day."})
    else:
        ex.append({"title":"Tongue twister warm-up","description":"Say 'She sells seashells' 5 times fast then slow. Builds articulation that carries into natural speech."})
    if wpm < 120:
        ex.append({"title":"Energy breathing","description":"Take a deep breath before each sentence and push your voice forward. Record and compare the difference."})
    elif wpm > 160:
        ex.append({"title":"Deliberate slow-read","description":"Read a paragraph at 80% your normal speed, pausing fully at every comma. Trains your brain to allow silence."})
    else:
        ex.append({"title":"Pace variation drill","description":"Read the same paragraph at three speeds: slow, normal, fast. Builds conscious control over your speaking rate."})
    ex.append({"title":"Mirror session","description":"Give a 30-second introduction without any filler words in front of a mirror. Restart every time you use one."})
    return ex


def hf_sentiment(transcript, token):
    try:
        r = requests.post(
            "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
            headers={"Authorization": f"Bearer {token}"},
            json={"inputs": transcript[:500]},
            timeout=10
        )
        data = r.json()
        if isinstance(data, list) and data[0]:
            best = max(data[0], key=lambda x: x["score"])
            return {"label": best["label"].capitalize(), "score": round(best["score"], 3)}
    except Exception as e:
        print(f"HF error: {e}")
    return None


def build_result(transcript, ta, af, sentiment, duration):
    mins, secs = int(duration // 60), int(duration % 60)
    return {
        "transcript": transcript,
        "duration": f"{mins:02d}:{secs:02d}",
        "duration_seconds": round(duration),
        "word_count": ta["word_count"],
        "wpm": ta["wpm"],
        "filler_count": ta["filler_count"],
        "filler_words": ta["filler_words"],
        "scores": ta["scores"],
        "ai_analysis": ta["ai_analysis"],
        "patterns": ta["patterns"],
        "therapy_recommended": ta["therapy_recommended"],
        "therapy_reason": ta["therapy_reason"],
        "exercises": ta["exercises"],
        "sentiment": sentiment,
        "audio_features": {
            "avg_pitch_hz": round(af["avg_pitch"], 1),
            "silence_ratio_pct": round(af["silence_ratio"] * 100, 1),
            "energy_variation": round(af["energy_std"], 4)
        }
    }


if __name__ == "__main__":
    print("=" * 60)
    print("VoiceLens Backend Server")
    print("=" * 60)
    print(f"Starting server on http://localhost:5001")
    print("Note: Whisper model will load on first analysis request")
    print("This may take 10-30 seconds for the first request")
    print("=" * 60)
    app.run(debug=True, port=5001, host='0.0.0.0')

# Made with Bob
