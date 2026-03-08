# VocalVitals Backend - FastAPI

## Project Overview
This is the FastAPI backend for VocalVitals Speech Emotion & Burnout Detection Platform. It handles audio analysis, emotion detection, burnout scoring, and voice journal management.

## Features
- 🎙️ Audio file upload and processing
- 😊 Emotion classification (7 emotions)
- 🔥 Burnout risk assessment
- 📊 Acoustic feature extraction
- 📔 Voice journal with SQLite database
- 📈 Trends and insights analytics
- 🔧 REST API with automatic documentation

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
# Or with uvicorn:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs` (Swagger UI)
ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Checks
- `GET /` - Service status
- `GET /api/health` - Module health check

### Audio Analysis
- `POST /api/audio/analyze` - Analyze uploaded audio file
  - Input: multipart/form-data (audio file)
  - Output: Emotion + Burnout Score + Acoustic Features

### Voice Journal
- `GET /api/entries?limit=50` - Get recent entries
- `GET /api/entries/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` - Date range query
- `POST /api/entries/add` - Save new entry

### Trends & Analytics
- `GET /api/trends/burnout?days=30` - Burnout trend chart data
- `GET /api/trends/emotions?days=30` - Emotion distribution
- `GET /api/insights?days=30` - AI insights and recommendations

## Project Structure

```
backend/
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
└── config.py        # Configuration settings

../src/              # Python modules (imported by main.py)
├── audio_processing/processor.py
├── feature_extraction/extractor.py
├── models/emotion_models.py
└── __init__.py

../database/
├── db.py            # SQLite database class
└── voice_journal.db # Database file
```

## Key Dependencies

Core:
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation

Audio Processing:
- `librosa==0.10.0` - Audio analysis (may have Python 3.13 issues)
- `soundfile==0.12.1` - Audio I/O
- `scipy==1.11.4` - Scientific computing

ML/Data:
- `scikit-learn==1.3.2` - Machine learning utilities
- `numpy==1.24.3` - Numerical computing
- `pandas==2.1.3` - Data manipulation

## Configuration

Edit `config.py`:
```python
HOST = "0.0.0.0"
PORT = 8000
ALLOWED_ORIGINS = ["http://localhost:4200", ...]
SAMPLE_RATE = 22050
MEL_BINS = 128
```

## Audio Analysis Pipeline

1. **Upload** - User uploads audio file (.wav, .mp3, .m4a, .ogg)
2. **Load** - AudioProcessor loads audio at 22050 Hz
3. **Features** - AcousticFeatureExtractor computes:
   - Jitter, Shimmer (voice quality)
   - Pitch, Energy (prosody)
   - MFCC, Zero-crossing rate (spectral)
   - Speech rate
4. **Emotion** - HybridEmotionModel predicts one of 7 emotions
5. **Burnout** - BurnoutClassifier scores burnout risk (0-100)
6. **Store** - Entry saved to SQLite database

## Emotion Classes

0: Neutral
1: Calm
2: Happy
3: Frustrated
4: Sad
5: Angry
6: Fearful

## Burnout Levels

- Healthy: 0-25
- Mild: 25-50
- Moderate: 50-75
- Severe: 75-100

## CORS Configuration

Configured for local development. For production:
1. Update `ALLOWED_ORIGINS` in code
2. Or set environment variables
3. Deploy behind reverse proxy (nginx, CloudFlare)

## Fallback Mode

If Librosa/TensorFlow modules fail to import, the API returns simulated responses so frontend development isn't blocked.

## Error Handling

- 400: Invalid audio file format
- 500: Processing error (check logs)
- CORS errors: Check `ALLOWED_ORIGINS`

## Development

```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Type checking
mypy main.py

# Linting
pylint main.py
```

## Troubleshooting

### Librosa ImportError
```bash
pip install --upgrade pip setuptools wheel
pip install librosa@0.10.0
```

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
# Or use different port:
python main.py --port 8001
```

### Database Issues
```bash
# Reset database
rm ../database/voice_journal.db
# Will be created on next run
```

## Production Deployment

```bash
# Using Gunicorn + Uvicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Using Docker
docker build -t vocalvitals-backend .
docker run -p 8000:8000 vocalvitals-backend

# Using Cloud Run (Google Cloud)
gcloud run deploy vocalvitals-backend --source .
```

## API Response Format

Emotion Analysis Response:
```json
{
  "emotion": {
    "label": "Happy",
    "confidence": 85.5,
    "all_emotions": { "Happy": 85.5, "Calm": 10.2, ... }
  },
  "burnout_score": 35.2,
  "burnout_level": "Mild",
  "stress_indicators": {
    "jitter": 0.0045,
    "shimmer": 0.08,
    "mean_pitch": 120.5,
    "pitch_variance": 450.2,
    "mean_energy": 0.42,
    "zero_crossing_rate": 0.12,
    "speech_rate": 2.1
  }
}
```

For full setup instructions, see `../FULLSTACK_SETUP.md`
