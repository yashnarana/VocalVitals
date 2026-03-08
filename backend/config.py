# Backend API Configuration

## FastAPI Server
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

## Allowed Origins (CORS)
ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular dev server
    "http://localhost:3000",  # Alternative frontend
    "http://127.0.0.1:4200",
]

## Database
DATABASE_PATH = "../database/voice_journal.db"

## Audio Processing
SAMPLE_RATE = 22050
MEL_BINS = 128
N_MFCC = 13
CHUNK_DURATION = 3.0  # seconds

## Model Configuration
EMOTION_CLASSES = 8  # RAVDESS emotions: Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprised
EMOTION_LABELS = [
    'Neutral',      # 01
    'Calm',         # 02
    'Happy',        # 03
    'Sad',          # 04
    'Angry',        # 05
    'Fearful',      # 06
    'Disgust',      # 07
    'Surprised'     # 08
]

## Burnout Scoring
BURNOUT_THRESHOLD = 50  # Score above 50 considered moderate-to-severe
