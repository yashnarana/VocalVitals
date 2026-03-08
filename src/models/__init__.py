"""
VocalVitals: Speech Emotion & Burnout Tracker
Deep Learning Models Module
"""

from .emotion_models import (
    create_feature_mlp,
    create_emotion_cnn,
    BurnoutClassifier,
    EMOTION_MAP,
    NUM_CLASSES,
)

__all__ = [
    'create_feature_mlp',
    'create_emotion_cnn',
    'BurnoutClassifier',
    'EMOTION_MAP',
    'NUM_CLASSES',
]
