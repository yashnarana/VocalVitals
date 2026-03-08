# VocalVitals - Full Stack Setup Guide

## Project Structure

```
VocalVitals/
├── frontend/                 # Angular 17 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/   # Page components (Home, Analyze, Journal, Trends, About)
│   │   │   ├── services/     # HTTP service for API calls
│   │   │   └── models/       # TypeScript interfaces
│   │   ├── main.ts           # Angular bootstrap
│   │   └── index.html        # Main HTML
│   ├── package.json
│   ├── angular.json
│   └── tsconfig.json
│
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── config.py            # Backend configuration
│
├── src/                      # Python modules (used by backend)
│   ├── audio_processing/    # Audio processing with Librosa
│   ├── feature_extraction/  # Acoustic biomarker extraction
│   ├── models/              # Deep learning models (TensorFlow/Keras)
│   └── __init__.py
│
├── database/
│   ├── db.py               # SQLite VoiceJournalDB class
│   └── voice_journal.db    # SQLite database file
│
├── config.py               # Global configuration
├── requirements.txt        # Python dependencies (Streamlit version)
└── README.md              # Full documentation
```

## Setup Instructions (macOS)

### 1. Prerequisites
```bash
# Install Node.js and npm (if not installed)
# Download from https://nodejs.org/ or use Homebrew:
brew install node

# Python 3.11+ should be installed
python3 --version
```

### 2. Backend Setup

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Note: If you encounter Librosa issues with Python 3.13, the backend has fallback responses
```

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Answer the prompts (select "y" for routing, "scss" for styling)
```

### 4. Running the Application

**Terminal 1 - Backend (FastAPI)**
```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals
source venv/bin/activate
cd backend
python main.py
# Or with uvicorn directly:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

**Terminal 2 - Frontend (Angular)**
```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals/frontend
ng serve
# Or with npm:
# npm start
```

Frontend will be available at: `http://localhost:4200`

### 5. Using the Application

1. Open browser to `http://localhost:4200`
2. Click "🎙️ Analyze Voice" to upload an audio file
3. View emotion detection and burnout score
4. Check "📔 Voice Journal" for all entries
5. View "📈 Trends & Insights" for patterns over time
6. Read "ℹ️ About" for more information

## API Endpoints

### Health & Status
- `GET /` - API status
- `GET /api/health` - Health check with module status

### Audio Analysis
- `POST /api/audio/analyze` - Analyze uploaded audio file
  - Input: Audio file (WAV, MP3, M4A)
  - Output: Emotion prediction + Burnout score + Acoustic features

### Voice Journal
- `GET /api/entries` - Get recent entries (default 50)
- `GET /api/entries/range` - Get entries by date range
- `POST /api/entries/add` - Save new entry to journal

### Trends & Analytics
- `GET /api/trends/burnout` - Get burnout trend (last N days)
- `GET /api/trends/emotions` - Get emotion distribution
- `GET /api/insights` - Get AI insights and recommendations

## API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Module Import Errors in Backend
If you see "ModuleNotFoundError: No module named 'src'", the backend will automatically return fallback responses. The Python modules are still available for direct use.

### Librosa Installation Issues
Librosa has compatibility issues with Python 3.13. The application will gracefully degrade with fallback responses:
```bash
# If Librosa fails to install, try:
pip install --upgrade pip setuptools wheel
```

### Port Already in Use
If ports 8000 or 4200 are already in use:

**Backend**: `python main.py --port 8001`
**Frontend**: `ng serve --port 4300`
Then update `AudioAnalysisService` to use the new backend port.

### CORS Issues
The backend already has CORS enabled for localhost. If you deploy, update the `ALLOWED_ORIGINS` in `backend/config.py`.

## Development Tips

### Frontend Development
- Use `ng serve` for hot reloading
- Check browser console (F12) for errors
- Use `ng generate component` to create new components
- Use `ng build --configuration production` for production build

### Backend Development
- Use `uvicorn main:app --reload` for auto-reload
- Check FastAPI docs at `/docs` for interactive testing
- Use `--log-level debug` for detailed logging

### Database
- SQLite database stored at `database/voice_journal.db`
- Schema includes: voice_entries, acoustic_features, daily_summaries tables
- For development, you can delete the database to reset: `rm database/voice_journal.db`

## Next Steps

1. **Customize Emotion Classes**: Edit `backend/config.py` and `frontend/src/app/services/audio-analysis.service.ts`
2. **Add Authentication**: Implement JWT tokens in FastAPI and Angular HTTP interceptors
3. **Deploy**: 
   - Backend: Docker container or Cloud Run
   - Frontend: Firebase Hosting or Netlify
4. **Production Build**:
   ```bash
   # Frontend
   ng build --configuration production
   
   # Backend
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
   ```

## Support & References

- Angular Documentation: https://angular.io/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- Librosa Documentation: https://librosa.org
- TensorFlow/Keras: https://www.tensorflow.org

---

**VocalVitals** - Speech Emotion & Burnout Detection Platform
