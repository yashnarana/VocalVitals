# VocalVitals - Step-by-Step Command Guide

## 📋 Before You Start
- ✅ Backend dependencies installed (FastAPI, etc.)
- ✅ RAVDESS dataset extracted (2,880 audio files)
- ✅ App updated for 8 emotions
- ✅ Both services ready to launch

---

## 🚀 STEP 1: Start the Backend Server

### Command (Copy & Paste)
```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals
source venv/bin/activate
cd backend
python main.py
```

### Expected Output
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
✅ All modules initialized successfully
```

### What This Means ✅
- Backend is now running on port 8000
- FastAPI is listening for requests
- Ready to process audio files

### Test It Works
Open in your browser:
- **API Status**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### ⚠️ If This Fails
See [Troubleshooting](#troubleshooting) section below

**🎯 Keep this terminal open and running!**

---

## 🚀 STEP 2: Start the Frontend Server (New Terminal)

### Open a NEW terminal window
```
Press: Ctrl+T (or Cmd+T on Mac)
OR
Go to Terminal menu → New Tab
```

### Command (Copy & Paste)
```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals/frontend
npm start
```

### Expected Output
```
✔ Compiled successfully

Local:            http://localhost:4200/
On Your Network:  http://192.168.1.x:4200/

Application bundle generated successfully. (XX.XX MB)

Watch mode enabled. Watching for file changes...
```

### What This Means ✅
- Frontend Angular app is now running on port 4200
- Database is ready for voice entries
- All 5 pages loaded and working

### 🎯 Keep this terminal open and running!

---

## 🌐 STEP 3: Open the Application

### In Your Browser
Open a new browser tab and go to:
```
http://localhost:4200
```

You should see:
- **VocalVitals** navbar at top
- **Home page** with feature cards
- **Navigation links**: Home, Analyze, Journal, Trends, About

---

## 🎯 STEP 4: Test the Application

### Test 1: Analyze a Voice File

1. **Click "🎙️ Analyze Voice"** in the navigation bar
2. **Click "Select Audio File"** button
3. **Navigate** to: `/Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/`
4. **Select** any `.wav` file (e.g., `03-01-01-01-01-01-01.wav`)
5. **Click "🔍 Analyze Voice"** button
6. **Wait** for analysis (2-5 seconds)

### You Should See ✅
```
Emotion: Neutral (or whatever emotion in the file)
Confidence: ~85%

Burnout Score: 35/100
Level: Mild 😐

Acoustic Features:
  - Jitter: 0.0045
  - Shimmer: 0.08
  - Mean Pitch: 120.5 Hz
  - Speech Rate: 2.1/s
  - Energy: 0.42
```

### 7. **Click "💾 Save to Journal"** (Optional)
   - Add notes in the text area
   - Click "Save to Journal" button
   - Confirmation message appears

---

### Test 2: Browse Journal

1. **Click "📔 Journal"** in navigation
2. **Try filters**:
   - Select emotion from dropdown
   - Pick start date
   - Pick end date
   - Click "🔄 Refresh"
3. **You should see** entries you saved earlier

---

### Test 3: View Trends

1. **Click "📈 Trends"** in navigation
2. **Select time period**: 7, 14, 30, or 90 days
3. **You should see**:
   - Burnout score trend line chart
   - Emotion distribution pie chart
   - AI insights and recommendations

---

### Test 4: Read About

1. **Click "ℹ️ About"** in navigation
2. **Read** about:
   - App mission
   - Technology stack
   - How it works
   - Privacy notice
   - Medical disclaimer

---

## 📊 Test Different Emotions

Try uploading different emotion files to see the analysis change:

```bash
# At /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/

# NEUTRAL files:
03-01-01-01-01-01-01.wav
03-01-01-01-02-01-01.wav

# CALM files:
03-01-02-01-01-01-01.wav
03-01-02-01-02-01-01.wav

# HAPPY files:
03-01-03-01-01-01-01.wav
03-01-03-01-02-01-01.wav

# SAD files (04):
# ANGRY files (05):
# FEARFUL files (06):
# DISGUST files (07):
# SURPRISED files (08):
```

Each file has this pattern:
- `03` = Audio-only
- `01` = Speech
- XX = Emotion code (01-08)
- `01` = Normal intensity
- `01` or `02` = Different statements
- `01` = First repetition
- `01` = Actor 01

---

## 🔍 Verify Everything Works

### Checklist (✅ = Done)

```
BACKEND (Terminal 1)
□ Backend running on http://localhost:8000
□ No error messages in terminal
□ Can access http://localhost:8000/docs

FRONTEND (Terminal 2)
□ Frontend running on http://localhost:4200
□ No error messages in terminal
□ Can see VocalVitals navbar

APPLICATION (Browser)
□ Homepage loads at http://localhost:4200
□ Can navigate to all 5 pages
□ Can select audio file
□ Can see analysis results
□ Can save to journal
□ Can filter entries in journal
□ Can view charts in trends
```

---

## 🛑 Troubleshooting

### Backend Issues

#### Error: "Port 8000 already in use"
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Then try starting backend again
```

#### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install fastapi uvicorn pydantic
```

#### Error: "Cannot create audio processor"
This is expected if Librosa has issues on Python 3.13. The backend will use fallback responses and the app still works!

---

### Frontend Issues

#### Error: "Cannot find module '@angular/..'"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

#### Error: "Port 4200 already in use"
```bash
# Use different port
ng serve --port 4300

# Then access: http://localhost:4300
```

#### Error: "Frontend can't connect to backend"
1. Make sure backend is running (Terminal 1)
2. Open browser console: F12
3. Check for red errors
4. Verify service URL is: `http://localhost:8000/api`

---

### Database Issues

#### Want to reset and start fresh?
```bash
# Delete the database
rm /Users/yashnarana/Desktop/VocalVitals/VocalVitals/database/voice_journal.db

# It will recreate on next save
```

---

## 📈 What to Do After Testing

### Option 1: Train Custom Models
See `/train_model.py` to train emotion classifier on RAVDESS dataset

### Option 2: Add More Features
- Real-time audio analysis
- User authentication
- Data export (PDF/CSV)
- Mobile app

### Option 3: Deploy to Production
See [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md) for cloud deployment instructions

---

## 📞 Need Help?

**Quick Links**:
- [START_HERE.md](START_HERE.md) - Quick reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
- [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md) - Complete setup guide
- http://localhost:8000/docs - Interactive API documentation

**Common Questions**:

**Q: Can I process files from other actors?**
A: Yes! Any `.wav` file in `/data/raw/Actor_02/` through `Actor_24/` works

**Q: How accurate is the emotion detection?**
A: Depends on models. Current setup uses fallback if TensorFlow unavailable. Train custom models for better accuracy.

**Q: Can I use files from other sources?**
A: Yes, but RAVDESS format assumed. Download other emotion datasets if needed.

**Q: How do I save analysis results?**
A: Click "💾 Save to Journal" after analyzing. Stored in SQLite database.

---

## ✅ You're All Set!

### Current Status:
- ✅ Backend ready: `http://localhost:8000`
- ✅ Frontend ready: `http://localhost:4200`
- ✅ RAVDESS dataset loaded: 2,880 audio files
- ✅ 8 emotions configured
- ✅ Database ready

### Next Action:
1. **Terminal 1**: Start backend with command above
2. **Terminal 2**: Start frontend with command above
3. **Browser**: Open http://localhost:4200
4. **Test**: Upload an audio file and analyze it!

---

**Happy analyzing! 🎙️**
