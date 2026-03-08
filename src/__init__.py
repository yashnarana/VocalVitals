"""
VocalVitals: Speech Emotion & Burnout Tracker
Main module initialization
"""

__version__ = "1.0.0"
__author__ = "VocalVitals Team"
__description__ = "AI-powered Speech Emotion & Burnout Tracker"

from src.audio_processing import AudioProcessor
from src.feature_extraction import AcousticFeatureExtractor
from src.models import (
    create_feature_mlp,
    create_emotion_cnn,
    BurnoutClassifier,
)
from database.db import VoiceJournalDB

__all__ = [
    'AudioProcessor',
    'AcousticFeatureExtractor',
    'create_feature_mlp',
    'create_emotion_cnn',
    'BurnoutClassifier',
    'VoiceJournalDB'
]
