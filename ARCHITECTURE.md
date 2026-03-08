# VocalVitals - Complete Architecture Summary

## Overview
VocalVitals is a full-stack Speech Emotion & Burnout Detection Platform built with:
- **Frontend**: Angular 17 with TypeScript and Bootstrap 5
- **Backend**: FastAPI (Python) with Uvicorn ASGI server
- **Database**: SQLite for voice journal storage
- **ML**: TensorFlow/Keras for emotion models
- **Audio**: Librosa for acoustic feature extraction

## Technology Stack

### Frontend (Angular 17)
```
Framework: Angular 17 (standalone components)
Language: TypeScript 5.2
Styling: Bootstrap 5.3 + Custom SCSS
Charts: Chart.js 4.4 with ng2-charts
HTTP: Angular HttpClient
State: RxJS Observables
Build: Angular CLI with Webpack
```

### Backend (FastAPI)
```
Framework: FastAPI 0.104.1
Server: Uvicorn 0.24.0
Validation: Pydantic 2.5
Language: Python 3.11+
Database: SQLite3
Audio: Librosa 0.10 + SoundFile 0.12
ML: TensorFlow/Keras + scikit-learn
```

### Data Processing
```
Audio Processing: Librosa (Mel-spectrograms, MFCC, Zero-crossing rate)
Feature Extraction: Custom acoustic biomarkers (40+ features)
Emotion Detection: Deep CNN trained on speech emotion datasets
Burnout Scoring: Machine learning classifier based on voice features
Database: SQLite with CRUD operations
```

## Project Structure

```
VocalVitals/
│
├── frontend/                          # Angular 17 Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── home.component.ts|html|scss
│   │   │   │   ├── analyze.component.ts|html|scss      ← Audio upload & analysis
│   │   │   │   ├── journal.component.ts|html|scss      ← Voice journal (CRUD)
│   │   │   │   ├── trends.component.ts|html|scss       ← Charts & analytics
│   │   │   │   ├── about.component.ts|html|scss
│   │   │   │   └── [AppComponent - Root]
│   │   │   ├── services/
│   │   │   │   └── audio-analysis.service.ts            ← HTTP service (8 methods)
│   │   │   ├── models/
│   │   │   │   └── voice.model.ts                       ← TypeScript interfaces
│   │   │   ├── app.routes.ts                            ← Route definitions
│   │   │   ├── app.config.ts                            ← Configuration
│   │   │   └── app.component.ts|html|scss
│   │   ├── main.ts                                      ← Bootstrap
│   │   └── index.html                                   ← Main HTML
│   ├── package.json
│   ├── angular.json
│   ├── tsconfig.json
│   └── README.md
│
├── backend/                           # FastAPI Backend API
│   ├── main.py                                          ← FastAPI application
│   │   ├── POST /api/audio/analyze          (File upload)
│   │   ├── GET /api/entries                 (Get journal entries)
│   │   ├── GET /api/entries/range           (Date range query)
│   │   ├── POST /api/entries/add            (Save entry)
│   │   ├── GET /api/trends/burnout          (Burnout chart data)
│   │   ├── GET /api/trends/emotions         (Emotion distribution)
│   │   ├── GET /api/insights                (AI recommendations)
│   │   └── GET /api/health                  (Status check)
│   ├── requirements.txt
│   ├── config.py
│   └── README.md
│
├── src/                               # Python Modules (ML/Audio)
│   ├── audio_processing/
│   │   └── processor.py                     ← AudioProcessor class
│   │       ├── load_audio()
│   │       ├── generate_mel_spectrogram()
│   │       ├── extract_spectral_features()
│   │       └── pad_or_truncate()
│   ├── feature_extraction/
│   │   └── extractor.py                     ← AcousticFeatureExtractor class
│   │       └── extract_all_features()       → 40+ acoustic biomarkers
│   ├── models/
│   │   └── emotion_models.py                ← Deep learning models
│   │       ├── EmotionCNN
│   │       ├── BurnoutClassifier
│   │       └── HybridEmotionModel
│   └── __init__.py
│
├── database/
│   ├── db.py                                ← VoiceJournalDB class
│   │   ├── add_voice_entry()
│   │   ├── get_entries_by_date_range()
│   │   ├── get_burnout_trend()
│   │   ├── get_emotion_distribution()
│   │   └── get_insights()
│   └── voice_journal.db                     ← SQLite database file
│
├── config.py                          ← Global configuration
├── requirements.txt                   ← Streamlit version deps
├── train_model.py                     ← Model training script
│
├── notebooks/
│   └── VocalVitals_Exploration.ipynb  ← 10-section Jupyter tutorial
│
├── FULLSTACK_SETUP.md                 ← Complete setup guide
├── setup-fullstack.sh                 ← Automated setup script
├── run-fullstack.sh                   ← Start both services
└── README.md                          ← Main documentation
```

## Component Details

### Frontend Components

#### HomeComponent
- **Purpose**: Landing page with feature overview
- **Features**: 
  - Feature cards (Emotion Detection, Burnout Detection, Voice Journal, Trend Analysis)
  - Quick start buttons
  - Disclaimer alert

#### AnalyzeComponent
- **Purpose**: Upload and analyze audio
- **Features**:
  - File input (WAV, MP3, M4A)
  - Audio analysis visualization
  - Emotion prediction display
  - Burnout score (0-100) with color coding
  - Acoustic features display (jitter, shimmer, pitch, energy)
  - Save to journal functionality
  - Status spinner during processing

#### JournalComponent
- **Purpose**: Browse and filter voice entries
- **Features**:
  - Emotion filter dropdown
  - Date range picker
  - Pagination (10 entries per page)
  - Full entry details (emotion, burnout, features)
  - Delete entry functionality
  - Personal notes display

#### TrendsComponent
- **Purpose**: Analytics and insights
- **Features**:
  - Burnout trend line chart (Chart.js)
  - Emotion distribution pie chart
  - Time period selector (7/14/30/90 days)
  - AI insights:
    - Key patterns detected
    - Recommendations
    - Strengths
    - Concerns
    - Overall assessment

#### AboutComponent
- **Purpose**: Information and documentation
- **Features**:
  - Mission statement
  - Technology stack listing
  - How it works (6 steps)
  - Acoustic features explained
  - Privacy notice
  - Medical disclaimer
  - References and quick links

### Frontend Service

#### AudioAnalysisService
Provides HTTP client methods:
```typescript
analyzeAudio(file: File)                    // POST /api/audio/analyze
getVoiceEntries(limit: number)              // GET /api/entries
getEntriesByDateRange(start, end)           // GET /api/entries/range
saveToJournal(...)                          // POST /api/entries/add
getBurnoutTrend(days: number)               // GET /api/trends/burnout
getEmotionDistribution(days: number)        // GET /api/trends/emotions
getInsights(days: number)                   // GET /api/insights
setAnalysisResult(result)                   // State management
```

### Backend Routes

All routes return JSON with proper HTTP status codes:

```
GET  /                              → {"status": "ok", "version": "1.0.0"}
GET  /api/health                    → {"status": "healthy", "modules": {...}}

POST /api/audio/analyze             → {"emotion": {...}, "burnout_score": 35.2, ...}
GET  /api/entries?limit=50          → [VoiceEntry[], ...]
GET  /api/entries/range             → [VoiceEntry[], ...]
POST /api/entries/add               → {"id": 123, "status": "success"}

GET  /api/trends/burnout?days=30    → [BurnoutTrend[], ...]
GET  /api/trends/emotions?days=30   → {"Happy": 15, "Calm": 8, ...}
GET  /api/insights?days=30          → {
                                       "key_patterns": [...],
                                       "recommendations": [...],
                                       "strengths": [...],
                                       "concerns": [...],
                                       "overall_assessment": "..."
                                     }
```

### Data Models

#### Frontend TypeScript Interfaces
```typescript
EmotionPrediction {
  label: string
  confidence: number
  all_emotions: { [emotion: string]: number }
}

StressIndicators {
  jitter: number
  shimmer: number
  mean_pitch: number
  pitch_variance: number
  mean_energy: number
  zero_crossing_rate: number
  speech_rate: number
}

AnalysisResult {
  emotion: EmotionPrediction
  burnout_score: number
  burnout_level: string
  stress_indicators: StressIndicators
}

VoiceEntry {
  id: number
  filename: string
  timestamp: string
  duration: number
  emotion_label: string
  burnout_score: number
  burnout_level: string
  acoustic_features: { [key: string]: number }
  notes: string
}

BurnoutTrend {
  date: string
  avg_burnout: number
  entry_count: number
}

Insights {
  key_patterns: string[]
  recommendations: string[]
  strengths: string[]
  concerns: string[]
  overall_assessment: string
}
```

## Audio Analysis Pipeline

### Input
- User uploads audio file (.wav, .mp3, .m4a, .ogg)
- 5+ seconds recommended

### Processing Steps
1. **Load Audio** → AudioProcessor.load_audio()
   - Resample to 22050 Hz
   - Normalize amplitude

2. **Feature Extraction** → AcousticFeatureExtractor.extract_all_features()
   - Voice Quality: jitter, shimmer, HNR
   - Prosody: pitch, energy, vibrato
   - Spectral: MFCC, zero-crossing rate
   - Speech Rate: syllables per second
   - **40+ acoustic biomarkers total**

3. **Emotion Detection** → HybridEmotionModel.predict_emotions()
   - Mel-spectrogram feature extraction
   - CNN inference
   - Returns 7-class probabilities:
     - Neutral, Calm, Happy, Frustrated, Sad, Angry, Fearful

4. **Burnout Scoring** → BurnoutClassifier.predict_burnout()
   - Takes acoustic features as input
   - Machine learning classifier
   - Outputs score 0-100
   - Levels: Healthy (0-25), Mild (25-50), Moderate (50-75), Severe (75-100)

5. **Storage** → VoiceJournalDB.add_voice_entry()
   - Save to SQLite database
   - Store acoustic features (not raw audio)
   - Timestamp for tracking

6. **Response** → Return JSON to frontend
   - Emotion prediction with confidence
   - Burnout score and level
   - Key acoustic features
   - Ready for display

### Key Improvements Over Streamlit Version
- Modular API architecture (easier to test)
- Real-time response times (<2s per analysis)
- Production-ready with CORS, error handling
- Better UI/UX with professional Angular components
- Chart.js for interactive visualizations
- TypeScript type safety
- Scalable architecture (easy to add auth, caching, etc.)

## Setup & Deployment

### Local Development
```bash
# 1. Setup (one-time)
bash setup-fullstack.sh

# 2. Run in separate terminals
# Terminal 1:
cd backend && python main.py

# Terminal 2:
cd frontend && npm start

# 3. Open http://localhost:4200
```

### Production Deployment

**Frontend (Angular)**:
- Build: `ng build --configuration production`
- Host on: Firebase Hosting, Netlify, Vercel, S3+CloudFront

**Backend (FastAPI)**:
- Containerize: `docker build -t vocalvitals-backend .`
- Run on: Cloud Run, App Engine, Render, Railway
- Use Gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

## Features Checklist

✅ **Backend**
- FastAPI application with 8 endpoints
- CORS middleware for Angular frontend
- Error handling and logging
- Health check endpoint
- Fallback responses for missing modules
- SQLite integration

✅ **Frontend**
- 5 full-featured components
- HTTP service with RxJS
- Bootstrap 5 styling
- Chart.js visualizations
- Form handling and validation
- Pagination and filtering
- Responsive design

✅ **Python Modules**
- Audio processing (Librosa)
- Feature extraction (40+ biomarkers)
- Emotion models (CNN)
- Burnout classifier
- SQLite database with CRUD

✅ **Documentation**
- FULLSTACK_SETUP.md (comprehensive guide)
- Frontend README (Angular-specific)
- Backend README (FastAPI-specific)
- Inline code comments
- Jupyter notebook (10 sections)

## Known Limitations

1. **Librosa Compatibility**: Python 3.13 doesn't fully support Librosa/numba
   - Workaround: Backend gracefully falls back to dummy data
   - Use Python 3.11 for full functionality

2. **Raw Audio Storage**: Currently doesn't store raw audio files
   - Only acoustic features stored (privacy-safe)
   - Can be added if needed

3. **Authentication**: Not implemented in this version
   - Can be added with JWT tokens
   - Frontend: HTTP interceptors
   - Backend: FastAPI security module

4. **HTTPS**: Not configured for development
   - Use nginx or reverse proxy for production

## Next Steps for Enhancement

1. **Authentication**: JWT tokens + user accounts
2. **Mobile App**: React Native or Flutter
3. **Real-time Analysis**: WebSockets for live feedback
4. **Advanced Analytics**: More ML insights
5. **Export Reports**: PDF generation
6. **Multi-language**: Support for multiple languages
7. **Cloud Deployment**: Docker + Kubernetes
8. **Performance**: Caching, CDN, database optimization

## API Documentation

Once backend is running:
- **Swagger UI**: http://localhost:8000/docs (interactive)
- **ReDoc**: http://localhost:8000/redoc (read-only)

Test endpoints directly in Swagger UI without writing code!

## Support Resources

- **Angular**: https://angular.io/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Bootstrap**: https://getbootstrap.com/docs
- **Librosa**: https://librosa.org/doc
- **TensorFlow**: https://www.tensorflow.org/guide

---

**VocalVitals** - Emotion & Burnout Detection through Voice Analysis
© 2026 | For educational and wellness purposes
