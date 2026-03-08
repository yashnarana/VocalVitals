"""
Deep Learning Models for Emotion & Burnout Classification
- Functional-API CNN for MFCC feature classification (easy to save/load)
- Rule-based burnout scorer from acoustic biomarkers
"""

import setuptools  # Must be imported before tensorflow for Python 3.12

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ── RAVDESS emotion mapping (8 classes) ──────────────────────────────
EMOTION_MAP = {
    0: "neutral",
    1: "calm",
    2: "happy",
    3: "sad",
    4: "angry",
    5: "fearful",
    6: "disgust",
    7: "surprised",
}

NUM_CLASSES = len(EMOTION_MAP)


# ─── 1. Feature-based MLP (primary model) ───────────────────────────
def create_feature_mlp(input_dim: int, num_classes: int = NUM_CLASSES) -> keras.Model:
    """
    Build a Functional-API MLP that takes a 1-D acoustic feature vector
    and predicts one of ``num_classes`` emotions.

    Architecture mirrors the proven layout from SER literature:
    Dense(512) → BN → Dropout → Dense(256) → BN → Dropout →
    Dense(128) → BN → Dropout → Dense(num_classes, softmax)
    """
    inp = keras.Input(shape=(input_dim,), name="features")

    x = layers.Dense(512, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4))(inp)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)

    x = layers.Dense(256, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)

    x = layers.Dense(128, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)

    out = layers.Dense(num_classes, activation="softmax", name="emotion")(x)

    model = keras.Model(inputs=inp, outputs=out, name="EmotionFeatureMLP")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ─── 2. CNN for Mel-spectrogram images  (optional / future) ─────────
def create_emotion_cnn(input_shape: tuple = (128, 128, 1),
                       num_classes: int = NUM_CLASSES) -> keras.Model:
    """
    Functional-API CNN that classifies emotion from log-Mel spectrograms.
    Conv2D blocks → GlobalAveragePooling → Dense head.
    """
    inp = keras.Input(shape=input_shape, name="mel_spectrogram")

    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(inp)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(256, (3, 3), activation="relu", padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.4)(x)

    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    out = layers.Dense(num_classes, activation="softmax", name="emotion")(x)

    model = keras.Model(inputs=inp, outputs=out, name="EmotionCNN")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ─── 3. Burnout scorer (rule-based) ─────────────────────────────────
class BurnoutClassifier:
    """
    Rule-based burnout scorer derived from acoustic stress indicators.
    Uses validated thresholds from speech pathology literature.
    """

    @staticmethod
    def predict_burnout(stress_indicators: dict) -> tuple:
        """Return (score 0-100, level_string)."""
        jitter = stress_indicators.get("jitter", 0)
        shimmer = stress_indicators.get("shimmer", 0)
        pitch_std = stress_indicators.get("pitch_std", 0)
        speech_rate = stress_indicators.get("speech_rate", 0)
        energy = stress_indicators.get("mean_energy", 0)

        score = 0.0
        score += min(jitter * 500, 25)
        score += min(shimmer * 50, 25)
        score += min(pitch_std / 10, 20)
        if energy > 0:
            score += max(0, 15 - energy * 100)
        if speech_rate > 0:
            score += min(abs(speech_rate - 4.0) * 3, 15)

        score = max(0.0, min(100.0, score))

        if score < 25:
            level = "Healthy"
        elif score < 50:
            level = "Mild"
        elif score < 75:
            level = "Moderate"
        else:
            level = "Severe"

        return score, level


# ─── 4. Convenience loader ──────────────────────────────────────────
def load_trained_model(model_path: str) -> keras.Model:
    """Load a saved Keras model from disk."""
    return keras.models.load_model(model_path)
