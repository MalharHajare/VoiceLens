# VoiceLens — AI Speech Confidence Coach
### LabLab IBM Bob Hackathon

> **Elegant maroon & purple themed UI** • **4 demo samples** • **Real-time speech analysis**

## 🎯 Features

- 🎤 **Live Recording** with real-time transcription (Web Speech API)
- 🔊 **Audio Analysis** using Librosa (pitch, energy, silence detection)
- 📝 **AI Transcription** with OpenAI Whisper
- 📊 **Smart Scoring** for fluency, clarity, pace, and confidence
- 🎨 **Filler Word Highlighting** in transcript
- 💬 **Sentiment Analysis** via Hugging Face API
- 🎭 **4 Demo Samples**: Moderate (US), Good (UK), Excellent (US), Severe (US - therapy recommended)
- 🎨 **Elegant UI** with maroon/purple color scheme (no neon)
- 🏥 **Therapy Recommendations** for severe cases
- 💪 **Personalized Exercises** based on your speech patterns

## 🚀 Stack

- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Live Transcription**: Web Speech API (Chrome/Edge)
- **Backend**: Python Flask server
- **AI Transcription**: OpenAI Whisper (runs locally, free)
- **Audio Analysis**: Librosa (pitch, pace, pauses, energy variation)
- **Sentiment**: Hugging Face Inference API (optional, free)
- **Built with**: IBM Bob AI Assistant

---

## ⚡ Quick Setup (5 minutes)

### Step 1 — Install Python dependencies
```bash
pip install flask flask-cors openai-whisper librosa numpy requests
```

> **Note:** Whisper requires ffmpeg:
> - **Mac**: `brew install ffmpeg`
> - **Ubuntu**: `sudo apt install ffmpeg`
> - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org)

### Step 2 — Run the Flask backend
```bash
python app_improved.py
```

You should see:
```
============================================================
VoiceLens Backend Server
============================================================
Starting server on http://localhost:5001
Note: Whisper model will load on first analysis request
This may take 10-30 seconds for the first request
============================================================
```

**Important:** The Whisper model loads lazily on the first analysis request (10-30 seconds), then subsequent analyses are fast.

### Step 3 — Open the frontend
Open `index.html` in **Google Chrome** or **Microsoft Edge** (Web Speech API requirement)

### Step 4 — Connect & Test
1. The status bar should show "Backend Online"
2. (Optional) Add a free [Hugging Face token](https://huggingface.co/settings/tokens) for sentiment analysis
3. Try one of the 4 demo samples or record your own voice!

---

---

## 🎭 Demo Samples

Choose from 4 pre-configured samples to see different analysis results:

| Sample | Description | Scores | Features |
|--------|-------------|--------|----------|
| **Moderate (US)** | Common speech patterns with fillers | Fluency: 42, Clarity: 65 | 14 filler words, needs improvement |
| **Good (UK)** | Professional British accent | Fluency: 85, Clarity: 88 | No fillers, strong delivery |
| **Excellent (US)** | Professional-grade speech | Fluency: 95, Clarity: 92 | Perfect control, zero fillers |
| **Severe (US)** | High disfluency, therapy needed | Fluency: 18, Clarity: 32 | 30+ fillers, anxiety indicators |

---

## 🔧 How It Works

1. **User clicks record** → Chrome's Web Speech API shows live transcript
2. **MediaRecorder** captures actual audio blob in background
3. **User selects demo sample** → Pre-configured transcript and analysis
4. **User clicks Analyze** → Audio blob POSTed to Flask `/analyse`
5. **Flask** saves audio to temp file
6. **Whisper** transcribes the audio with high accuracy
7. **Librosa** extracts audio features:
   - Average pitch (Hz)
   - Energy variation
   - Silence ratio
   - Speaking pace
8. **Python logic** calculates scores:
   - Fluency (filler word ratio)
   - Clarity (sentence structure)
   - Pace (words per minute)
   - Confidence (composite score)
9. **Filler detection** highlights problematic words
10. **Pattern analysis** identifies speech issues
11. **Therapy recommendation** for severe cases
12. **Hugging Face** (optional) runs sentiment analysis
13. **JSON result** sent back to frontend
14. **Frontend** renders:
    - Color-coded scores with progress bars
    - Highlighted transcript (fillers in red)
    - Speech patterns with severity badges
    - Personalized exercises
    - Therapy alert if needed

---

## 📡 API Endpoints

### `GET /`
Health check endpoint

**Returns:**
```json
{
  "status": "VoiceLens backend running",
  "model_status": "ready|loading|not_loaded",
  "error": null
}
```

### `GET /health`
Detailed health status

**Returns:**
```json
{
  "healthy": true,
  "model_loaded": true,
  "model_loading": false,
  "model_error": null
}
```

### `POST /analyse`
Analyze audio file for speech patterns

**Form Data:**
- `audio` — Audio file (webm, mp3, wav, etc.)
- `hf_token` — (Optional) Hugging Face API token for sentiment
- `demo_mode` — (Optional) Use demo analysis

**Returns:**
```json
{
  "transcript": "Your transcribed speech...",
  "duration": "00:45",
  "duration_seconds": 45,
  "word_count": 112,
  "wpm": 149,
  "filler_count": 8,
  "filler_words": ["um", "uh", "like", "you know"],
  "scores": {
    "fluency": 72,
    "clarity": 78,
    "pace": 85,
    "confidence": 76
  },
  "ai_analysis": "Detailed AI-generated feedback...",
  "patterns": [
    {
      "label": "High filler word use",
      "severity": "high",
      "description": "8 fillers detected (7% ratio) — ideal is under 3%."
    }
  ],
  "therapy_recommended": false,
  "therapy_reason": "Your speech is progressing well...",
  "exercises": [
    {
      "title": "Silent pause drill",
      "description": "Record yourself for 60 seconds..."
    }
  ],
  "sentiment": {
    "label": "Positive",
    "score": 0.94
  },
  "audio_features": {
    "avg_pitch_hz": 187.3,
    "silence_ratio_pct": 12.4,
    "energy_variation": 0.0234
  }
}
```

---

## 📁 Project Structure

```
voicelens/
├── app_improved.py      # Flask backend with lazy loading
├── index.html           # Frontend UI with 4 demo samples
├── style.css            # Maroon/purple themed styles
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
└── .venv/              # Virtual environment (created during setup)
```

---

## 🎨 UI Features

- **Elegant Color Scheme**: Maroon and purple tones (no neon)
- **Real-time Waveform**: Visual feedback during recording
- **Live Transcript**: See your words as you speak
- **Animated Scores**: Progress bars with color coding
- **Filler Highlighting**: Red background on problematic words
- **Severity Badges**: Visual indicators for speech patterns
- **Responsive Design**: Works on desktop and mobile

---

## 🏥 Therapy Recommendations

The system recommends professional speech therapy when:
- Filler word ratio exceeds 12%
- Speaking pace is extremely fast (>200 wpm) or slow (<80 wpm)
- Severe disfluency patterns are detected
- Speech anxiety indicators are present

---

## 🎯 For Hackathon Demo

1. **Start backend**: `python app_improved.py`
2. **Open frontend**: Double-click `index.html` in Chrome
3. **Show demo samples**:
   - Select "Excellent (US)" → Show perfect scores
   - Select "Severe (US)" → Show therapy recommendation
   - Select "Good (UK)" → Show British accent analysis
4. **Record live**: Demonstrate real-time transcription
5. **Highlight features**:
   - Librosa audio analysis
   - Filler word detection
   - Personalized exercises
   - IBM Bob's role in development

---

## 🤖 Built with IBM Bob

IBM Bob AI Assistant was instrumental in:
- Scaffolding the project structure
- Implementing lazy model loading
- Creating the elegant UI design
- Generating sample data variants
- Debugging and optimization
- Documentation and code quality

---

## 📝 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ for LabLab IBM Bob Hackathon**
