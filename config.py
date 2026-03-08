"""
Configuration settings for VocalVitals
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
DATABASE_DIR = PROJECT_ROOT / "database"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, DATABASE_DIR, NOTEBOOKS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Audio processing configuration
AUDIO_CONFIG = {
    'sample_rate': 22050,
    'n_mels': 128,
    'n_fft': 2048,
    'hop_length': 512,
    'n_mfcc': 13,
    'target_duration': 3.0  # seconds
}

# Model configuration
MODEL_CONFIG = {
    'emotion_classes': 8,  # RAVDESS: neutral, calm, happy, sad, angry, fearful, disgust, surprised
    'emotion_labels': ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fearful', 'Disgust', 'Surprised'],
    'burnout_classes': 4,  # healthy, mild, moderate, severe
    'burnout_labels': ['Healthy', 'Mild', 'Moderate', 'Severe'],
    'cnn_input_shape': (128, 128, 1),
    'feature_vector_size': 41  # 40 acoustic features
}

# Training configuration
TRAINING_CONFIG = {
    'batch_size': 32,
    'epochs': 100,
    'validation_split': 0.2,
    'learning_rate': 0.001,
    'early_stopping_patience': 10
}

# Database configuration
DATABASE_CONFIG = {
    'db_path': str(DATABASE_DIR / 'voice_journal.db'),
    'max_audio_duration': 300,  # 5 minutes max
}

# Feature extraction configuration
FEATURE_CONFIG = {
    'jitter_frame_length': 2048,
    'shimmer_frame_length': 2048,
    'voice_activity_threshold': 0.02,
    'pitch_estimation_method': 'piptrack'  # or 'pyin'
}

# Burnout score thresholds
BURNOUT_THRESHOLDS = {
    'healthy': (0, 25),
    'mild': (25, 50),
    'moderate': (50, 75),
    'severe': (75, 100)
}

# Backend URLs (for future cloud integration)
API_CONFIG = {
    'api_url': os.getenv('VOCALVITALS_API_URL', 'http://localhost:5000'),
    'upload_endpoint': '/api/upload',
    'analyze_endpoint': '/api/analyze'
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': PROJECT_ROOT / 'logs' / 'vocalvitals.log'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# Ensure logs directory exists
LOGS_DIR = PROJECT_ROOT / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print("VocalVitals Configuration")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Models Directory: {MODELS_DIR}")
    print(f"Database: {DATABASE_CONFIG['db_path']}")
    print(f"\nAudio Config: {AUDIO_CONFIG}")
    print(f"Model Config: {MODEL_CONFIG}")
    print(f"Training Config: {TRAINING_CONFIG}")
