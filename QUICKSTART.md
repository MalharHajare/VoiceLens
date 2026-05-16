# VoiceLens Quick Start Guide

## ✅ Ready to Launch!

Your VoiceLens AI Speech Coach is configured and ready to analyze speech patterns.

## 🎨 What's New

- ✨ **Elegant maroon/purple UI** (no neon colors)
- 🎭 **4 demo samples** with different speech patterns
- 🔴 **Filler word highlighting** in transcripts
- 🏥 **Therapy recommendations** for severe cases
- 📊 **Fixed score displays** with proper color coding
- 🎯 **Personalized exercises** based on performance

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Backend Server

```bash
cd /Users/malharhajare/Downloads/voicelens
source .venv/bin/activate
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

**💡 Tip:** The Whisper model loads lazily on the first analysis (10-30 seconds), then subsequent analyses are fast (2-5 seconds).

### Step 2: Open the Frontend

```bash
open index.html
```

Or double-click `index.html` in Finder. **Use Chrome or Edge** for best results (Web Speech API requirement).

### Step 3: Try the Demo Samples

1. **Check connection**: Status bar should show "Backend Online" 🟢
2. **Select a demo sample** from the dropdown:
   - **Moderate (US)** - Common speech with fillers
   - **Good (UK)** - Professional British accent
   - **Excellent (US)** - Perfect delivery
   - **Severe (US)** - Needs therapy (worst case)
3. **Click "Load Selected Sample"**
4. **Click "✦ Analyze Speech"**
5. **View results**: Scores, highlighted transcript, patterns, exercises

## 🎭 Demo Sample Guide

| Sample | What It Shows | Best For |
|--------|---------------|----------|
| **Moderate (US)** | 14 filler words, needs improvement | Showing typical user case |
| **Good (UK)** | British accent, no fillers, strong scores | Demonstrating good performance |
| **Excellent (US)** | Professional-grade, 95+ scores | Showing ideal speech |
| **Severe (US)** | 30+ fillers, therapy alert | Demonstrating therapy recommendation |

## 🎤 Record Your Own Voice

1. Click the **purple record button**
2. Allow microphone access when prompted
3. Speak naturally for 30-90 seconds
4. Click again to stop recording
5. Click **"✦ Analyze Speech"**
6. Wait for results (first analysis takes longer)

## 🎨 Understanding the Results

### Score Cards
- **Green (70+)**: Excellent performance
- **Orange (50-69)**: Needs improvement
- **Red (<50)**: Requires significant work

### Filler Words
Highlighted in **red** with light red background in the transcript:
- um, uh, like, you know, basically, etc.

### Speech Patterns
- **Low severity** (green badge): Good habits
- **Mid severity** (orange badge): Areas to improve
- **High severity** (red badge): Priority issues

### Therapy Alert
- **Green box**: Self-practice recommended
- **Red box**: Professional therapy may help

## 🔧 Advanced Usage

### Add Hugging Face Token (Optional)
For sentiment analysis:
1. Get free token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Paste in "Hugging Face Token" field
3. Click "Save"
4. Sentiment will appear in results

### Check Server Status
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "healthy": true,
  "model_loaded": true,
  "model_loading": false,
  "model_error": null
}
```

### Restart Server
If needed:
1. Press `Ctrl+C` in terminal
2. Run: `python app_improved.py`

## 🐛 Troubleshooting

### Backend Offline
**Problem**: Status shows "Backend Offline"

**Solutions**:
1. Check if server is running in terminal
2. Verify URL is `http://localhost:5001`
3. Click "Connect" button
4. Check firewall settings

### Port Already in Use
**Problem**: Error "Address already in use"

**Solution**:
```bash
# Find and kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in app_improved.py line 296
```

### Model Loading Fails
**Problem**: First analysis times out

**Solutions**:
1. Check internet connection (first download)
2. Wait full 30 seconds for model load
3. Check terminal for error messages
4. Verify ffmpeg is installed: `ffmpeg -version`

### Microphone Not Working
**Problem**: Recording doesn't start

**Solutions**:
1. Use Chrome or Edge browser
2. Allow microphone permission when prompted
3. Check system microphone settings
4. Try refreshing the page

### Scores Not Displaying
**Problem**: Scores show as "—"

**Solution**: Refresh browser - CSS classes are now fixed!

## 📊 What Gets Analyzed

### Audio Features (Librosa)
- **Average Pitch**: Vocal frequency in Hz
- **Silence Ratio**: Percentage of pauses
- **Energy Variation**: Voice dynamics

### Text Analysis (Python)
- **Word Count**: Total words spoken
- **Filler Count**: Um, uh, like, etc.
- **Words Per Minute**: Speaking pace
- **Sentence Structure**: Clarity scoring

### AI Analysis (Whisper + Custom Logic)
- **Fluency Score**: Based on filler ratio
- **Clarity Score**: Sentence structure quality
- **Pace Score**: WPM vs ideal range (120-160)
- **Confidence Score**: Composite metric

## 💡 Pro Tips

1. **First Analysis**: Takes 10-30 seconds (model loading)
2. **Subsequent Analyses**: Only 2-5 seconds
3. **Best Results**: Speak for 30-90 seconds
4. **Quiet Environment**: Reduces background noise
5. **Natural Speech**: Don't over-rehearse
6. **Try All Samples**: See different analysis types

## 📁 Project Files

```
voicelens/
├── app_improved.py      # Flask backend (use this!)
├── index.html           # Frontend with 4 samples
├── style.css            # Maroon/purple theme
├── requirements.txt     # Dependencies
├── README.md           # Full documentation
├── QUICKSTART.md       # This guide
└── .venv/              # Virtual environment
```

## 🎯 For Presentations/Demos

### Quick Demo Flow (2 minutes)
1. **Show UI**: "Elegant maroon/purple theme"
2. **Select "Excellent"**: "Perfect speech example"
3. **Analyze**: "See 95+ scores"
4. **Select "Severe"**: "Therapy recommendation"
5. **Show Features**: Filler highlighting, exercises

### Full Demo Flow (5 minutes)
1. **Start with "Moderate"**: Typical user
2. **Show "Good (UK)"**: British accent
3. **Record Live**: Real-time transcription
4. **Show "Severe"**: Therapy alert
5. **Explain Tech**: Whisper, Librosa, IBM Bob

## 🤖 IBM Bob's Contributions

IBM Bob helped with:
- ✅ Project scaffolding and structure
- ✅ Lazy model loading implementation
- ✅ UI design and color scheme
- ✅ Sample data generation
- ✅ Bug fixes and optimization
- ✅ Documentation writing

## 🔗 Useful Links

- **Whisper**: [github.com/openai/whisper](https://github.com/openai/whisper)
- **Librosa**: [librosa.org](https://librosa.org)
- **Hugging Face**: [huggingface.co](https://huggingface.co)
- **Web Speech API**: [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

---

## ✨ You're All Set!

**Server**: 🟢 http://localhost:5001
**Frontend**: Open `index.html` in Chrome
**Samples**: 4 variants ready to test

**Enjoy analyzing speech with VoiceLens!** 🎤✨

---

*Made with ❤️ for LabLab IBM Bob Hackathon*