"""
VocalVitals – RAVDESS Model Training Pipeline  (TensorFlow / Keras)
Extracts rich acoustic features from the RAVDESS dataset and trains
a Keras MLP for emotion classification.

Usage:
    python train_ravdess.py
"""

import setuptools  # Must be imported before tensorflow on Python 3.12

import os
import sys
import glob
import time
import json
import warnings
from pathlib import Path

import numpy as np
import librosa

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).parent))
from src.models.emotion_models import create_feature_mlp

warnings.filterwarnings("ignore")

# ─── Constants ───────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data" / "raw"
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

EMOTION_MAP = {
    1: "neutral",
    2: "calm",
    3: "happy",
    4: "sad",
    5: "angry",
    6: "fearful",
    7: "disgust",
    8: "surprised",
}

SR = 22050          # Target sample rate
DURATION = 3.0      # Seconds to use per clip (pad / truncate)
N_MFCC = 40         # Number of MFCC coefficients
BATCH_SIZE = 32
EPOCHS = 150        # EarlyStopping will halt well before this


# ─── 1. Dataset Loading ─────────────────────────────────────────────
def discover_ravdess_files(data_dir: Path) -> list:
    """Walk data_dir, find all *.wav matching RAVDESS naming, parse labels."""
    records = []
    wav_files = sorted(glob.glob(str(data_dir / "**" / "*.wav"), recursive=True))

    for fpath in wav_files:
        fname = os.path.basename(fpath)
        parts = fname.replace(".wav", "").split("-")
        if len(parts) != 7:
            continue

        modality, vocal_ch, emotion_id, intensity, statement, rep, actor = (
            int(p) for p in parts
        )

        # Keep speech files only (vocal_channel == 01)
        if vocal_ch != 1:
            continue

        records.append(
            {
                "path": fpath,
                "modality": modality,
                "vocal_channel": vocal_ch,
                "emotion_id": emotion_id,
                "emotion": EMOTION_MAP.get(emotion_id, "unknown"),
                "intensity": intensity,
                "statement": statement,
                "repetition": rep,
                "actor": actor,
                "gender": "female" if actor % 2 == 0 else "male",
            }
        )

    return records


# ─── 2. Feature Extraction ──────────────────────────────────────────
def extract_features(file_path: str, sr: int = SR,
                     duration: float = DURATION) -> np.ndarray:
    """
    Extract a comprehensive feature vector (~188 dims) from one audio file.

    Includes:
      - 40 MFCCs: mean + std  (80)
      - 40 delta-MFCCs: mean + std  (80)
      - 12 chroma mean
      - 7 spectral-contrast mean
      - spectral centroid / bandwidth / rolloff / ZCR / RMS  (5)
      - pitch mean + std  (2)
      - jitter + shimmer  (2)
    """
    y, _ = librosa.load(file_path, sr=sr, duration=duration)

    # Pad / truncate to fixed length
    target_len = int(sr * duration)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]

    feats = []

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
    amps = [float(np.sqrt(np.mean(y[i*hop_length:i*hop_length+frame_length]**2)))
            for i in range(min(n_frames, 60))]
    amps = np.array(amps)
    shimmer = (float(np.mean(np.abs(np.diff(amps))) / np.mean(amps))
               if len(amps) > 1 and np.mean(amps) > 0 else 0.0)
    feats.append(shimmer)

    return np.array(feats, dtype=np.float64)


def build_feature_matrix(records: list) -> tuple:
    """Extract features for every record; return (X, y_strings)."""
    X_list, y_list = [], []
    total = len(records)

    for i, rec in enumerate(records):
        if i % 200 == 0:
            print(f"  Extracting features … {i}/{total}")
        try:
            feat = extract_features(rec["path"])
            X_list.append(feat)
            y_list.append(rec["emotion"])
        except Exception as e:
            print(f"  ⚠ Skipping {rec['path']}: {e}")

    X = np.array(X_list)
    y = np.array(y_list)
    print(f"  ✅ Feature matrix: {X.shape}  |  Labels: {y.shape}")
    return X, y


# ─── 3. Data Augmentation (feature-space) ───────────────────────────
def augment_features(X: np.ndarray, y: np.ndarray,
                     noise_std: float = 0.015,
                     n_copies: int = 2) -> tuple:
    """
    Simple augmentation by adding Gaussian noise to feature vectors.
    Helps the model generalise and not overfit on a ~1400-sample dataset.
    """
    X_aug = [X]
    y_aug = [y]
    for _ in range(n_copies):
        noise = np.random.normal(0, noise_std, X.shape)
        X_aug.append(X + noise)
        y_aug.append(y)
    return np.concatenate(X_aug), np.concatenate(y_aug)


# ─── 4. Training ────────────────────────────────────────────────────
def train_model(X: np.ndarray, y: np.ndarray):
    """
    Train the TensorFlow / Keras Feature-MLP.
    Returns (model, scaler, label_encoder, test_accuracy).
    """
    # Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    num_classes = len(le.classes_)
    y_cat = to_categorical(y_enc, num_classes=num_classes)

    # Train / test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_cat, test_size=0.2, random_state=42,
        stratify=y_enc,
    )

    # Also split encoded labels for metrics later
    _, _, ye_train, ye_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42,
        stratify=y_enc,
    )

    # Feature-space augmentation on training set only
    print("  Augmenting training data …")
    X_train_aug, y_train_aug = augment_features(X_train, y_train, n_copies=2)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_aug)
    X_test_scaled = scaler.transform(X_test)

    # Replace any nan / inf that might have crept in
    X_train_scaled = np.nan_to_num(X_train_scaled)
    X_test_scaled = np.nan_to_num(X_test_scaled)

    print(f"\n  Train (augmented): {X_train_scaled.shape[0]}  |  "
          f"Test: {X_test_scaled.shape[0]}  |  Classes: {num_classes}")
    print(f"  Feature dim: {X_train_scaled.shape[1]}\n")

    # Build model
    model = create_feature_mlp(
        input_dim=X_train_scaled.shape[1],
        num_classes=num_classes,
    )
    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor="val_accuracy",
            patience=20,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=8,
            min_lr=1e-6,
            verbose=1,
        ),
        ModelCheckpoint(
            str(MODEL_DIR / "emotion_model_best.keras"),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]

    # Class weights to handle imbalanced neutral class (fewer samples)
    unique, counts = np.unique(np.argmax(y_train_aug, axis=1), return_counts=True)
    total_samples = len(y_train_aug)
    class_weight = {
        int(cls): total_samples / (num_classes * cnt)
        for cls, cnt in zip(unique, counts)
    }
    print(f"  Class weights: {class_weight}\n")

    # Train
    history = model.fit(
        X_train_scaled, y_train_aug,
        validation_data=(X_test_scaled, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        class_weight=class_weight,
        verbose=1,
    )

    # Evaluate
    loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
    print(f"\n  ✅ Test accuracy : {accuracy:.4f}")
    print(f"     Test loss     : {loss:.4f}")

    # Per-class report
    y_pred = np.argmax(model.predict(X_test_scaled, verbose=0), axis=1)
    from sklearn.metrics import classification_report
    print("\n" + classification_report(
        ye_test, y_pred, target_names=le.classes_
    ))

    return model, scaler, le, accuracy, history


# ─── 5. Save Artefacts ──────────────────────────────────────────────
def save_artefacts(model, scaler, label_encoder, model_dir: Path = MODEL_DIR):
    """Save model, scaler, label encoder, and class-name mapping."""
    model.save(str(model_dir / "emotion_model.keras"))

    import joblib
    joblib.dump(scaler, model_dir / "feature_scaler.joblib")
    joblib.dump(label_encoder, model_dir / "label_encoder.joblib")

    # Also save a plain-JSON class map for easy inspection
    class_map = {int(i): str(c) for i, c in enumerate(label_encoder.classes_)}
    with open(model_dir / "class_map.json", "w") as f:
        json.dump(class_map, f, indent=2)

    print(f"\n  💾 Model        → {model_dir / 'emotion_model.keras'}")
    print(f"  💾 Scaler       → {model_dir / 'feature_scaler.joblib'}")
    print(f"  💾 LabelEncoder → {model_dir / 'label_encoder.joblib'}")
    print(f"  💾 Class map    → {model_dir / 'class_map.json'}")


# ─── 6. Main ────────────────────────────────────────────────────────
def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   VocalVitals — RAVDESS Model Training  (TensorFlow/Keras)   ║
    ║   Speech Emotion Detection                                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    # Step 1 — Discover
    print("📂 Step 1: Discovering RAVDESS audio files …")
    records = discover_ravdess_files(DATA_DIR)
    print(f"   Found {len(records)} speech files\n")

    if not records:
        print("❌ No RAVDESS files found under", DATA_DIR)
        sys.exit(1)

    emotion_counts = {}
    for r in records:
        emotion_counts[r["emotion"]] = emotion_counts.get(r["emotion"], 0) + 1
    print("   Emotion distribution:")
    for emo, cnt in sorted(emotion_counts.items()):
        print(f"     {emo:12s} → {cnt}")
    print()

    # Step 2 — Extract features
    print("🎵 Step 2: Extracting acoustic features …")
    t0 = time.time()
    X, y = build_feature_matrix(records)
    print(f"   Feature extraction took {time.time() - t0:.1f}s\n")

    # Step 3 — Train
    print("🧠 Step 3: Training TensorFlow model …")
    model, scaler, le, test_acc, history = train_model(X, y)
    print()

    # Step 4 — Save
    print("💾 Step 4: Saving artefacts …")
    save_artefacts(model, scaler, le)

    print(f"""
    ════════════════════════════════════════════════════════════════
    ✅  Training complete!

    Test accuracy : {test_acc:.2%}
    Model saved to: {MODEL_DIR / 'emotion_model.keras'}
    ════════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    main()
