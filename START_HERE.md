# 🚀 VocalVitals - Start Here Guide

## Dataset Information ✅

Your RAVDESS dataset has been successfully extracted:
- **Location**: `/data/raw/Actor_01/` through `Actor_24/`
- **Total Files**: 2,880 audio files
- **Format**: WAV files with standardized naming convention
- **Actors**: 24 professional actors (12 male, 12 female)

### RAVDESS Emotions (8 Total)
The app has been updated to support all 8 RAVDESS emotions:

| Code | Emotion | Example Filename | Emoji |
|------|---------|-------------------|-------|
| 01 | Neutral | 03-01-01-01-01-01-01.wav | 😐 |
| 02 | Calm | 03-01-02-01-01-01-01.wav | 😌 |
| 03 | Happy | 03-01-03-01-01-01-01.wav | 😊 |
| 04 | Sad | 03-01-04-01-01-01-01.wav | 😢 |
| 05 | Angry | 03-01-05-01-01-01-01.wav | 😠 |
| 06 | Fearful | 03-01-06-01-01-01-01.wav | 😨 |
| 07 | Disgust | 03-01-07-01-01-01-01.wav | 🤢 |
| 08 | Surprised | 03-01-08-01-01-01-01.wav | 😲 |

### Filename Format Breakdown
Each file: `03-01-06-01-02-01-12.wav`
- **03** = Audio-only (03 = audio-only, 02 = video-only, 01 = full AV)
- **01** = Speech (01 = speech, 02 = song)
- **06** = Fearful emotion
- **01** = Normal intensity (01 = normal, 02 = strong)
- **02** = Statement "Dogs are sitting by the door"
- **01** = 1st repetition
- **12** = Actor 12 (Female, since even number)

---

## ✅ App Configuration Updated

Your application has been automatically updated to match RAVDESS:
- ✅ Backend emotion map: 8 emotions
- ✅ Frontend emotion filter: 8 emotions  
- ✅ Config files: Updated for RAVDESS structure
- ✅ Emotion icons: Added for Disgust 🤢 and Surprised 😲

---

## 🔧 Run the Application

### Terminal 1: Start Backend (FastAPI)

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals
source venv/bin/activate
cd backend
python main.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     ✅ All modules initialized successfully
```

✅ **Backend Ready** — Navigate to:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Terminal 2: Start Frontend (Angular)

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals/frontend
npm start
```

**You should see:**
```
✔ Compiled successfully.
  Application bundle generated successfully.
  Local: http://localhost:4200
```

✅ **Frontend Ready** — Open browser: http://localhost:4200

---

## 💡 What to Do Next

### 1. Test Audio Analysis
1. Open http://localhost:4200
2. Click "🎙️ Analyze Voice" in navigation
3. Click "Select Audio File"
4. Navigate to `/Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/`
5. Select any `.wav` file (e.g., `03-01-01-01-01-01-01.wav`)
6. Click "🔍 Analyze Voice"
7. View results (emotion prediction + burnout score)
8. Click "💾 Save to Journal"

### 2. Browse Voice Journal
1. Click "📔 Journal" in navigation
2. Filter by emotion using dropdown
3. Set date range with calendar pickers
4. Click through pages

### 3. View Trends
1. Click "📈 Trends" in navigation
2. Select time period (7/14/30/90 days)
3. View burnout trend chart
4. View emotion distribution pie chart
5. Read AI insights

### 4. Learn More
1. Click "ℹ️ About" page
2. Read technology information
3. Understand how it works

---

## 📊 Testing Different Emotions

Try uploading files with different emotions to test the system:

```bash
# Navigate to dataset
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/

# Files by emotion (Actor_01):
ls 03-01-01* # Neutral
ls 03-01-02* # Calm
ls 03-01-03* # Happy
ls 03-01-04* # Sad
ls 03-01-05* # Angry
ls 03-01-06* # Fearful
ls 03-01-07* # Disgust
ls 03-01-08* # Surprised
```

Example tests:
- Upload a Happy file → Should detect Happy emotion
- Upload a Sad file → Should detect Sad emotion
- Upload an Angry file → Should detect Angry emotion

---

## 🔍 Verify Everything Works

### Checklist

- [ ] **Backend Running**: http://localhost:8000 shows JSON response
- [ ] **API Docs Available**: http://localhost:8000/docs loads
- [ ] **Frontend Running**: http://localhost:4200 loads homepage
- [ ] **Navigation Works**: Can click between all 5 pages
- [ ] **File Upload Works**: Can select audio file in Analyze page
- [ ] **Analysis Works**: Can analyze audio and see results
- [ ] **Burnout Score Displays**: Shows 0-100 score with color
- [ ] **Journal Saves**: Can save entries and see them in Journal
- [ ] **Filtering Works**: Can filter by emotion and date in Journal
- [ ] **Charts Load**: Trends page shows burnout trend and emotion pie chart

---

## 🐛 Troubleshooting

### Backend won't start (Port 8000 already in use)
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>

# Or use different port - edit backend/main.py:
# Change: uvicorn.run(app, host="0.0.0.0", port=8000)
# To:     uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend won't compile
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Can't connect frontend to backend
1. Make sure backend is running on port 8000
2. Open browser console (F12)
3. Check for CORS errors
4. Verify URL in `frontend/src/app/services/audio-analysis.service.ts`
   - Should be: `http://localhost:8000/api`

### Audio file not uploading
- File must be in WAV, MP3, M4A, or OGG format
- File should be 5+ seconds long
- Try using files from `/data/raw/Actor_01/` for testing

---

## 📁 Quick File Locations

```
Project Root:
/Users/yashnarana/Desktop/VocalVitals/VocalVitals/

Audio Data:
/Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/ → Actor_24/

Backend:
/Users/yashnarana/Desktop/VocalVitals/VocalVitals/backend/

Frontend:
/Users/yashnarana/Desktop/VocalVitals/VocalVitals/frontend/

Database:
/Users/yashnarana/Desktop/VocalVitals/VocalVitals/database/voice_journal.db (created on first run)
```

---

## 🎯 Next Steps (Optional)

1. **Train Models** (Optional)
   - See `train_model.py` for training custom emotion classifier on RAVDESS data
   - Requires more setup but improves accuracy

2. **Deploy to Production**
   - See `FULLSTACK_SETUP.md` for deployment instructions
   - Frontend: Firebase Hosting, Netlify, Vercel
   - Backend: Cloud Run, Render, Railway

3. **Add More Features**
   - User authentication
   - Data export (PDF, CSV)
   - Real-time analysis with WebSocket
   - Mobile app with React Native

---

## ✅ Summary of Changes Made

1. ✅ Extracted RAVDESS dataset (2,880 audio files)
2. ✅ Updated emotion classes from 7 to 8
3. ✅ Updated backend emotion mapping
4. ✅ Updated frontend emotion arrays
5. ✅ Added emoji support for new emotions
6. ✅ Installed FastAPI and dependencies
7. ✅ Ready for immediate use

---

## 📞 Need Help?

**Documentation Files:**
- [FULLSTACK_SETUP.md](FULLSTACK_SETUP.md) - Complete setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [backend/README.md](backend/README.md) - Backend API docs
- [frontend/README.md](frontend/README.md) - Frontend Angular docs

**Key Endpoints:**
- `http://localhost:8000/docs` - Interactive API documentation (Swagger UI)
- `http://localhost:4200` - Application frontend

---

**Status**: ✅ Ready to run!

**Next Action**: Open 2 terminals and follow the commands above to start the backend and frontend. Then navigate to http://localhost:4200 to use the app!
