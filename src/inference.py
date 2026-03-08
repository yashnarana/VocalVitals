"""
VocalVitals — Inference module
Loads trained model artefacts and runs emotion prediction on audio files.
"""

import setuptools  # Must be imported before tensorflow on Python 3.12

import os
import json
import numpy as np
import librosa
import joblib
import tensorflow as tf
from tensorflow import keras
from pathlib import Path

from src.models.emotion_models import BurnoutClassifier

# ─── Constants (must match training) ─────────────────────────────────
SR = 22050
DURATION = 3.0
N_MFCC = 40

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


# ─── Feature extraction (mirrors train_ravdess.extract_features) ────
def extract_features(file_path: str, sr: int = SR,
                     duration: float = DURATION) -> np.ndarray:
    """
    Extract the same ~188-dim feature vector used during training.
    """
    y, _ = librosa.load(file_path, sr=sr, duration=duration)

    target_len = int(sr * duration)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]

    feats: list = []

    # MFCCs & deltas
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    feats.extend(np.mean(mfcc, axis=1))
    feats.extend(np.std(mfcc, axis=1))
    delta_mfcc = librosa.feature.delta(mfcc)
    feats.extend(np.mean(delta_mfcc, axis=1))
    feats.extend(np.std(delta_mfcc, axis=1))

    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    feats.extend(np.mean(chroma, axis=1))

    # Spectral contrast
    spec_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    feats.extend(np.mean(spec_contrast, axis=1))

    # Scalar spectral features
    feats.append(float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))))
    feats.append(float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))))
    feats.append(float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))))
    feats.append(float(np.mean(librosa.feature.zero_crossing_rate(y))))
    feats.append(float(np.mean(librosa.feature.rms(y=y))))

    # Pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_vals = []
    for t in range(pitches.shape[1]):
        idx = magnitudes[:, t].argmax()
        p = pitches[idx, t]
        if p > 0:
            pitch_vals.append(p)
    pitch_vals = np.array(pitch_vals) if pitch_vals else np.array([0.0])
    feats.append(float(np.mean(pitch_vals)))
    feats.append(float(np.std(pitch_vals)))

    # Jitter
    if len(pitch_vals) > 1 and np.mean(pitch_vals) > 0:
        jitter = float(np.mean(np.abs(np.diff(pitch_vals))) / np.mean(pitch_vals))
    else:
        jitter = 0.0
    feats.append(jitter)

    # Shimmer
    frame_length, hop_length = 2048, 512
    n_frames = max(1, (len(y) - frame_length) // hop_length + 1)
    amps = [float(np.sqrt(np.mean(y[i * hop_length:i * hop_length + frame_length] ** 2)))
            for i in range(min(n_frames, 60))]
    amps = np.array(amps)
    shimmer = (float(np.mean(np.abs(np.diff(amps))) / np.mean(amps))
               if len(amps) > 1 and np.mean(amps) > 0 else 0.0)
    feats.append(shimmer)

    return np.array(feats, dtype=np.float64)


def extract_stress_indicators(file_path: str, sr: int = SR,
                              duration: float = DURATION) -> dict:
    """
    Extract human-readable stress indicators from audio.
    Returns a dict with jitter, shimmer, pitch stats, energy, ZCR, speech_rate.
    """
    y, _ = librosa.load(file_path, sr=sr, duration=duration)

    target_len = int(sr * duration)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]

    # Pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_vals = []
    for t in range(pitches.shape[1]):
        idx = magnitudes[:, t].argmax()
        p = pitches[idx, t]
        if p > 0:
            pitch_vals.append(p)
    pitch_vals = np.array(pitch_vals) if pitch_vals else np.array([0.0])

    mean_pitch = float(np.mean(pitch_vals))
    pitch_std = float(np.std(pitch_vals))

    # Jitter
    if len(pitch_vals) > 1 and mean_pitch > 0:
        jitter = float(np.mean(np.abs(np.diff(pitch_vals))) / mean_pitch)
    else:
        jitter = 0.0

    # Shimmer
    frame_length, hop_length = 2048, 512
    n_frames = max(1, (len(y) - frame_length) // hop_length + 1)
    amps = [float(np.sqrt(np.mean(y[i * hop_length:i * hop_length + frame_length] ** 2)))
            for i in range(min(n_frames, 60))]
    amps = np.array(amps)
    shimmer = (float(np.mean(np.abs(np.diff(amps))) / np.mean(amps))
               if len(amps) > 1 and np.mean(amps) > 0 else 0.0)

    # Energy / ZCR
    mean_energy = float(np.mean(librosa.feature.rms(y=y)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))

    # Speech rate (onset-based syllable estimate)
    try:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        from scipy import signal as scipy_signal
        peaks = scipy_signal.find_peaks(onset_env, height=np.median(onset_env))[0]
        duration_sec = len(y) / sr
        speech_rate = len(peaks) / duration_sec if duration_sec > 0 else 0.0
    except Exception:
        speech_rate = 0.0

    return {
        "jitter": round(jitter, 6),
        "shimmer": round(shimmer, 6),
        "mean_pitch": round(mean_pitch, 2),
        "pitch_variance": round(pitch_std ** 2, 2),
        "pitch_std": round(pitch_std, 2),
        "mean_energy": round(mean_energy, 6),
        "zero_crossing_rate": round(zcr, 6),
        "speech_rate": round(speech_rate, 2),
    }


# ─── Model / artefact loading ───────────────────────────────────────
class EmotionPredictor:
    """Wraps trained model + scaler + label encoder for one-call inference."""

    def __init__(self, model_dir: Path = MODEL_DIR):
        self.model_dir = model_dir

        model_path = model_dir / "emotion_model.keras"
        scaler_path = model_dir / "feature_scaler.joblib"
        le_path = model_dir / "label_encoder.joblib"
        class_map_path = model_dir / "class_map.json"

        if not model_path.exists():
            raise FileNotFoundError(f"Trained model not found at {model_path}")

        self.model = keras.models.load_model(str(model_path))
        self.scaler = joblib.load(str(scaler_path))
        self.label_encoder = joblib.load(str(le_path))

        with open(class_map_path) as f:
            self.class_map = json.load(f)  # {"0": "angry", ...}

    def predict(self, file_path: str) -> dict:
        """
        Run full inference on an audio file.

        Returns:
            dict with keys:
                label       – predicted emotion string
                confidence  – float 0-100
                all_emotions – {emotion: probability%}
        """
        feats = extract_features(file_path)
        feats_scaled = self.scaler.transform(feats.reshape(1, -1))
        probs = self.model.predict(feats_scaled, verbose=0)[0]

        top_idx = int(np.argmax(probs))
        label = self.class_map.get(str(top_idx), self.label_encoder.classes_[top_idx])
        confidence = float(probs[top_idx]) * 100

        all_emotions = {}
        for i, p in enumerate(probs):
            name = self.class_map.get(str(i), self.label_encoder.classes_[i])
            all_emotions[name.capitalize()] = round(float(p) * 100, 2)

        return {
            "label": label.capitalize(),
            "confidence": round(confidence, 2),
            "all_emotions": all_emotions,
        }
