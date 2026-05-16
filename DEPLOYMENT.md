# VoiceLens Deployment Guide

## 🚨 Important: Backend Limitations

VoiceLens uses **OpenAI Whisper** (49MB+ model) and **Librosa** for audio analysis, which require:
- Large model files (exceeds Vercel's 50MB limit)
- Long processing times (10-30 seconds for first request)
- Significant memory and CPU resources
- Python runtime with ML libraries

**Vercel's serverless functions have:**
- 50MB deployment size limit
- 10-second execution timeout (Hobby), 60s (Pro)
- Limited memory for ML models

Therefore, we use a **hybrid deployment strategy**:
- ✅ **Frontend on Vercel** (static HTML/CSS/JS)
- ⚠️ **Backend on alternative platforms** (see options below)

---

## 🎯 Deployment Strategy

### Option 1: Frontend-Only Demo (Vercel)
Deploy the frontend to Vercel with **demo mode only** (no real audio analysis).

**Pros:**
- ✅ Free and instant deployment
- ✅ Works immediately with 4 demo samples
- ✅ Perfect for showcasing UI and features
- ✅ No backend maintenance needed

**Cons:**
- ❌ Cannot analyze real audio recordings
- ❌ Demo mode only (pre-configured samples)

### Option 2: Full Stack (Vercel + Railway/Render)
Deploy frontend to Vercel, backend to a Python-friendly platform.

**Pros:**
- ✅ Full functionality with real audio analysis
- ✅ Scalable and production-ready
- ✅ Separate frontend/backend scaling

**Cons:**
- ⚠️ Backend requires paid hosting ($5-10/month)
- ⚠️ More complex setup

### Option 3: All-in-One (Railway/Render)
Deploy both frontend and backend together on one platform.

**Pros:**
- ✅ Simplest setup
- ✅ Full functionality
- ✅ Single deployment

**Cons:**
- ⚠️ Requires paid hosting
- ⚠️ Less optimized than separate deployments

---

## 📦 Option 1: Frontend-Only on Vercel (Recommended for Demo)

### Step 1: Prepare Repository
```bash
# Ensure you have these files:
# - index.html
# - style.css
# - vercel.json
# - .vercelignore
# - README.md
```

### Step 2: Deploy to Vercel

#### Method A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd /Users/malharhajare/Downloads/voicelens
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? voicelens
# - Directory? ./
# - Override settings? No
```

#### Method B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your Git repository (GitHub/GitLab/Bitbucket)
4. Or drag & drop the project folder
5. Click "Deploy"

### Step 3: Configure Frontend
After deployment, your site will be at `https://voicelens.vercel.app`

The frontend will work in **demo mode** with 4 sample analyses:
- ✅ Moderate (US) - Needs Improvement
- ✅ Good (UK) - Strong Performance
- ✅ Excellent (US) - Professional
- ✅ Severe (US) - Therapy Recommended

**Note:** The "Record" button will work for UI demonstration, but analysis will use local fallback (no real Whisper transcription).

---

## 🚀 Option 2: Full Stack Deployment

### Frontend: Vercel (Free)
Follow Option 1 steps above.

### Backend: Choose One Platform

#### A. Railway (Recommended - $5/month)

**Why Railway?**
- ✅ Easy Python deployment
- ✅ Automatic HTTPS
- ✅ Environment variables
- ✅ Good free tier (500 hours/month)
- ✅ Scales automatically

**Steps:**

1. **Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Create `Procfile`:**
```
web: python app.py
```

3. **Update `app.py` for production:**
```python
# Change the last line to:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, port=port, host='0.0.0.0')
```

4. **Deploy:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Get URL
railway domain
```

5. **Update Frontend:**
Edit `index.html` line 36:
```html
<input type="text" id="backendUrl" value="https://your-app.railway.app" placeholder="Backend URL">
```

#### B. Render (Free tier available)

**Why Render?**
- ✅ Free tier (with limitations)
- ✅ Auto-deploy from Git
- ✅ Easy setup

**Steps:**

1. **Create `render.yaml`:**
```yaml
services:
  - type: web
    name: voicelens-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    envVars:
      - key: PORT
        value: 10000
```

2. **Update `app.py`:**
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, port=port, host='0.0.0.0')
```

3. **Deploy:**
- Go to [render.com](https://render.com)
- Connect your Git repository
- Select "Web Service"
- Render will auto-detect Python
- Click "Create Web Service"

4. **Update Frontend:**
Use your Render URL: `https://voicelens-backend.onrender.com`

#### C. Fly.io (Good for ML workloads)

**Why Fly.io?**
- ✅ Better for ML/AI apps
- ✅ More memory options
- ✅ Global deployment

**Steps:**

1. **Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Create `fly.toml`:**
```toml
app = "voicelens"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

3. **Deploy:**
```bash
fly launch
fly deploy
```

---

## 🔧 Option 3: All-in-One Deployment

### Railway (Easiest)

1. **Add static file serving to `app.py`:**
```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)
```

2. **Deploy to Railway** (see Option 2A steps)

3. **Access at:** `https://your-app.railway.app`

---

## 🌐 Environment Variables

For production deployments, set these environment variables:

```bash
# Optional: Hugging Face token for sentiment analysis
HF_TOKEN=hf_xxxxxxxxxxxxx

# Port (usually auto-set by platform)
PORT=5001

# Flask environment
FLASK_ENV=production
```

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid Plan | Best For |
|----------|-----------|-----------|----------|
| **Vercel** | ✅ Unlimited (frontend only) | $20/mo | Static sites, demos |
| **Railway** | 500 hrs/mo ($5 credit) | $5/mo + usage | Full-stack Python apps |
| **Render** | ✅ 750 hrs/mo (sleeps after 15min) | $7/mo | Hobby projects |
| **Fly.io** | 3 VMs free | $1.94/mo + usage | ML/AI workloads |

---

## 🚀 Quick Deploy Commands

### Frontend Only (Vercel)
```bash
cd /Users/malharhajare/Downloads/voicelens
vercel --prod
```

### Full Stack (Railway)
```bash
# Frontend
vercel --prod

# Backend
railway up
railway domain
```

### All-in-One (Railway)
```bash
railway up
railway domain
```

---

## ✅ Post-Deployment Checklist

- [ ] Frontend deployed and accessible
- [ ] Backend deployed (if using Option 2/3)
- [ ] Backend URL updated in `index.html`
- [ ] CORS configured correctly
- [ ] Demo samples working
- [ ] Live recording tested (if backend deployed)
- [ ] Sentiment analysis working (if HF token added)
- [ ] Mobile responsive design verified
- [ ] HTTPS enabled
- [ ] Custom domain configured (optional)

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem:** "Backend Offline" message
- ✅ Check backend URL in settings
- ✅ Ensure backend is deployed and running
- ✅ Check CORS headers
- ✅ Try demo mode (works without backend)

**Problem:** Demo samples not working
- ✅ Clear browser cache
- ✅ Check browser console for errors
- ✅ Ensure JavaScript is enabled

### Backend Issues

**Problem:** "Model loading failed"
- ✅ Check platform memory limits
- ✅ Ensure ffmpeg is installed
- ✅ Check deployment logs
- ✅ Verify requirements.txt is correct

**Problem:** Timeout errors
- ✅ First request takes 10-30s (model loading)
- ✅ Increase timeout limits in platform settings
- ✅ Use lazy loading (already implemented)

**Problem:** Out of memory
- ✅ Upgrade to paid plan with more RAM
- ✅ Use smaller Whisper model (tiny/base)
- ✅ Optimize audio processing

---

## 📝 Recommended Setup for Hackathon Demo

**Best approach for showcasing:**

1. **Deploy frontend to Vercel** (free, instant)
   - Shows beautiful UI
   - Demo samples work perfectly
   - No backend needed

2. **Run backend locally during demo**
   - Full functionality
   - No deployment costs
   - Easy to debug

3. **Demo flow:**
   - Show 4 demo samples on Vercel
   - Switch to localhost for live recording demo
   - Highlight the hybrid architecture

**Commands:**
```bash
# Deploy frontend
vercel --prod

# Run backend locally for demo
python app.py

# Update frontend to use localhost
# (or keep Vercel URL for demo samples only)
```

---

## 🎯 Production Recommendations

For a production deployment:

1. **Frontend:** Vercel (free, fast, reliable)
2. **Backend:** Railway ($5/mo, easy Python deployment)
3. **Database:** Add PostgreSQL for user history (optional)
4. **Monitoring:** Add Sentry for error tracking
5. **Analytics:** Add Google Analytics or Plausible

**Estimated monthly cost:** $5-10

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Fly.io Documentation](https://fly.io/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🆘 Need Help?

If you encounter issues:

1. Check platform-specific logs
2. Verify environment variables
3. Test locally first
4. Check CORS configuration
5. Review deployment documentation

---

**Made with ❤️ for LabLab IBM Bob Hackathon**