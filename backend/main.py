import setuptools  # Must be before tensorflow for Python 3.12 compatibility

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging
import os
import sys
import warnings

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── Trained model inference ──────────────────────────────────────────
try:
    from src.inference import EmotionPredictor, extract_stress_indicators
    from src.models.emotion_models import BurnoutClassifier
    INFERENCE_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    INFERENCE_AVAILABLE = False
    warnings.warn(f"Inference module not available: {e}")
    EmotionPredictor = None
    BurnoutClassifier = None

try:
    from database.db import VoiceJournalDB
    DB_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    DB_AVAILABLE = False
    warnings.warn(f"Database not available: {e}")
    VoiceJournalDB = None


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="VocalVitals API",
    description="Speech Emotion & Burnout Detection API",
    version="1.0.0"
)

# Configure CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:4200", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize modules ──────────────────────────────────────────────
emotion_predictor = None
burnout_classifier = None
db = None

try:
    if INFERENCE_AVAILABLE:
        emotion_predictor = EmotionPredictor()
        burnout_classifier = BurnoutClassifier()
        logger.info("✅ Trained emotion model loaded successfully")
    else:
        logger.warning("⚠️ Inference module not available — running in demo mode")

    if DB_AVAILABLE:
        db = VoiceJournalDB()
        logger.info("✅ Database connected")
    else:
        logger.warning("⚠️ Database not available")

except Exception as e:
    logger.warning(f"⚠️ Module initialization warning: {e}")
    emotion_predictor = None
    burnout_classifier = None
    db = None

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "ok",
        "service": "VocalVitals API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/audio/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analyze uploaded audio file for emotion and burnout indicators.
    Uses the trained TensorFlow/Keras model when available.
    """
    try:
        if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.ogg')):
            raise HTTPException(status_code=400, detail="Invalid audio file format")

        # Save temporary file
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if emotion_predictor is None:
            # Fallback response with dummy data (model not loaded)
            result = {
                "emotion": {
                    "label": "Neutral",
                    "confidence": 75.0,
                    "all_emotions": {
                        "Neutral": 75.0, "Calm": 10.0, "Happy": 5.0,
                        "Sad": 3.0, "Angry": 2.0, "Fearful": 2.0,
                        "Disgust": 1.5, "Surprised": 1.5,
                    }
                },
                "burnout_score": 35.5,
                "burnout_level": "Mild",
                "stress_indicators": {
                    "jitter": 0.0045, "shimmer": 0.08,
                    "mean_pitch": 120.5, "pitch_variance": 450.2,
                    "mean_energy": 0.42, "zero_crossing_rate": 0.12,
                    "speech_rate": 2.1,
                }
            }
            os.remove(temp_path)
            return result

        # ── Real inference ───────────────────────────────────────────
        # 1. Emotion prediction (trained Keras model)
        emotion_result = emotion_predictor.predict(temp_path)

        # 2. Stress indicators (acoustic biomarkers)
        stress = extract_stress_indicators(temp_path)

        # 3. Burnout score (rule-based from stress indicators)
        burnout_score, burnout_level = burnout_classifier.predict_burnout(stress)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "emotion": emotion_result,
            "burnout_score": round(float(burnout_score), 2),
            "burnout_level": burnout_level,
            "stress_indicators": stress,
        }

    except Exception as e:
        logger.error(f"Error analyzing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entries")
async def get_entries(limit: int = 50):
    """Get recent voice entries"""
    try:
        if db is None:
            return []
        entries = db.get_latest_entries(limit=limit)
        # Convert DataFrame to list of dicts for JSON response
        if hasattr(entries, 'to_dict'):
            return entries.to_dict(orient='records')
        return entries
    except Exception as e:
        logger.error(f"Error fetching entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entries/range")
async def get_entries_range(start_date: str, end_date: str):
    """Get entries within a date range"""
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        entries = db.get_entries_by_date_range(start, end)
        return entries
    except Exception as e:
        logger.error(f"Error fetching entries by range: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/entries/add")
async def save_entry(
    filename: str,
    duration: float,
    emotion_label: str,
    burnout_score: float,
    burnout_level: str,
    acoustic_features: dict,
    notes: str = ""
):
    """Save voice entry to journal"""
    try:
        entry_id = db.add_voice_entry(
            filename=filename,
            duration=duration,
            emotion_label=emotion_label,
            burnout_score=burnout_score,
            burnout_level=burnout_level,
            acoustic_features=acoustic_features,
            notes=notes
        )
        return {"id": entry_id, "status": "success"}
    except Exception as e:
        logger.error(f"Error saving entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/burnout")
async def get_burnout_trend(days: int = 30):
    """Get burnout trend over time"""
    try:
        trend = db.get_burnout_trend(days=days)
        return trend
    except Exception as e:
        logger.error(f"Error fetching burnout trend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/emotions")
async def get_emotion_distribution(days: int = 30):
    """Get emotion distribution"""
    try:
        distribution = db.get_emotion_distribution(days=days)
        return distribution
    except Exception as e:
        logger.error(f"Error fetching emotion distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights")
async def get_insights(days: int = 30):
    """Get AI insights based on recent entries"""
    try:
        if db is None:
            return {
                "avg_burnout_score": 0,
                "highest_burnout_day": None,
                "emotion_distribution": {},
                "avg_jitter": 0,
                "avg_shimmer": 0,
                "total_entries": 0,
            }
        insights = db.get_insights(days=days)
        return insights
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        # Return safe defaults instead of 500
        return {
            "avg_burnout_score": 0,
            "highest_burnout_day": None,
            "emotion_distribution": {},
            "avg_jitter": 0,
            "avg_shimmer": 0,
            "total_entries": 0,
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "emotion_predictor": emotion_predictor is not None,
            "burnout_classifier": burnout_classifier is not None,
            "database": db is not None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
