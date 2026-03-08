# VocalVitals: Speech Emotion & Burnout Tracker

![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)

An AI-powered platform that detects emotional state and burnout indicators through voice analysis. VocalVitals combines deep learning (CNNs on Mel-spectrograms), signal processing, and acoustic biomarkers to provide real-time insights into mental health.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Dataset (RAVDESS)](#dataset-ravdess)
- [Training Models](#training-models)
- [API Reference](#api-reference)
- [Acoustic Features Explained](#acoustic-features-explained)
- [Burnout Score](#burnout-score)
- [Privacy & Disclaimers](#privacy--disclaimers)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## Features

- **Real-time Voice Analysis** — Upload or record audio for instant emotion detection
- **Burnout Detection** — Quantifies stress via acoustic biomarkers (jitter, shimmer, pitch variability)
- **Voice Journal** — Stores all recordings with emotional and stress metadata (SQLite)
- **Trend Visualization** — Track emotional and burnout patterns over days/weeks/months
- **AI-Powered Insights** — Actionable recommendations based on voice patterns
- **Privacy First** — All data stored locally, no cloud uploads
- **Hybrid Model** — CNN spectrogram analysis + acoustic feature classification

---

## How It Works

```
Audio Input (.wav / .mp3 / .m4a)
    │
    ├──► Audio Processing ──► Mel-Spectrogram
    │
    ├──► Feature Extraction ──► 40+ Acoustic Biomarkers
    │
    ├──► CNN Spectrogram Classifier ──► Emotion Prediction
    │
    ├──► Burnout Classifier ──► Burnout Score (0–100)
    │
    └──► Voice Journal DB ──► Trends & Insights Dashboard
```

### Key Biomarkers

| Biomarker | What It Measures | Burnout Signal |
|-----------|-----------------|----------------|
| Jitter | Frequency instability | Higher = more stressed |
| Shimmer | Amplitude variation | Higher = more fatigued |
| Pitch Std Dev | Pitch variability | Lower = emotional flattening |
| Voice Activity | Speaking proportion | Lower = exhaustion |
| Speech Rate | Syllables/second | Changes indicate stress |
| Energy | Voice loudness | Lower = burnout |

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **ML/DL** | TensorFlow/Keras, Scikit-learn |
| **Audio** | Librosa, NumPy, SciPy, SoundFile |
| **Backend** | FastAPI, Uvicorn, Pydantic, SQLite |
| **Frontend** | Streamlit (dashboard), Angular 17 (full-stack option) |
| **Data** | Pandas, Matplotlib, Seaborn |
| **Dev** | Jupyter Notebooks, Google Colab (GPU training) |

---

## Project Structure

```
VocalVitals/
├── app/
│   └── main.py                        # Streamlit dashboard
├── backend/
│   ├── main.py                        # FastAPI application (8 REST endpoints)
│   ├── config.py                      # Backend configuration
│   └── requirements.txt               # Backend Python dependencies
├── src/
│   ├── audio_processing/
│   │   └── processor.py               # Audio loading, Mel-spectrogram generation
│   ├── feature_extraction/
│   │   └── extractor.py               # Jitter, shimmer, pitch, energy (40+ features)
│   ├── models/
│   │   └── emotion_models.py          # EmotionCNN, BurnoutClassifier, HybridModel
│   ├── inference.py                   # Model inference utilities
│   └── utils/
│       └── download_datasets.py       # Dataset download helpers
├── database/
│   └── db.py                          # SQLite VoiceJournalDB class
├── models/                            # Trained model weights (.keras, .joblib)
│   ├── emotion_model.keras
│   ├── emotion_model_best.keras
│   ├── feature_scaler.joblib
│   ├── label_encoder.joblib
│   └── class_map.json
├── data/
│   ├── raw/                           # RAVDESS audio files (Actor_01–Actor_24)
│   └── processed/                     # Processed spectrograms
├── notebooks/
│   └── VocalVitals_Exploration.ipynb  # EDA & prototyping
├── frontend/                          # Streamlit frontend pages
│   ├── app.py
│   ├── api_client.py
│   └── pages/                         # Home, Analyze, Journal, Trends, About
├── config.py                          # Global configuration
├── train_model.py                     # Model training script
├── train_ravdess.py                   # RAVDESS-specific training script
├── verify_environment.py              # Environment validation utility
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup
└── README.md                          # This file
```

---

## Installation

### Prerequisites

- Python 3.8+ (3.10–3.12 recommended for full TensorFlow/Librosa support)
- pip package manager
- ~2 GB free disk space (for datasets)
- Node.js & npm (only if using Angular frontend)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yashnarana/VocalVitals.git
cd VocalVitals

# 2. Create and activate a virtual environment (Python 3.12 recommended)
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

> **Note (Python 3.12+ compatibility):** Always import `setuptools` before `tensorflow`:
> ```python
> import setuptools  # Must be first
> import tensorflow as tf
> ```

---

## Quick Start

### Option A: Streamlit Dashboard

```bash
streamlit run app/main.py
# Opens at http://localhost:8501
```

### Option B: FastAPI Backend + Frontend

**Terminal 1 — Backend:**
```bash
.venv/bin/python backend/main.py
# API running at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

**Terminal 2 — Frontend (Streamlit):**
```bash
source .venv/bin/activate
streamlit run frontend/app.py
# Opens at http://localhost:8501
```

### Using the App

1. Navigate to **Analyze Voice**
2. **Record your voice** using the built-in microphone, or upload a `.wav`, `.mp3`, or `.m4a` file
3. View results: emotion prediction, burnout score, acoustic features, Mel-spectrogram
4. Save to **Voice Journal** for tracking
5. Check **Trends** for patterns over time

---

## Dataset (RAVDESS)

VocalVitals uses the **RAVDESS** (Ryerson Audio-Visual Database of Emotional Speech and Song) dataset.

| Property | Value |
|----------|-------|
| Total Files | 2,880 audio files |
| Actors | 24 (12 male, 12 female) |
| Emotions | 8: Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprised |
| Intensities | Normal + Strong (except Neutral) |
| Format | WAV, 16-bit, 48 kHz |
| Location | `data/raw/Actor_01/` through `Actor_24/` |

### Filename Convention

Each file follows the pattern: `03-01-06-01-02-01-12.wav`

| Position | Example | Meaning |
|----------|---------|---------|
| 1 | 03 | Modality (03 = audio-only) |
| 2 | 01 | Channel (01 = speech) |
| 3 | 06 | **Emotion** (see table below) |
| 4 | 01 | Intensity (01 = normal, 02 = strong) |
| 5 | 02 | Statement (01 or 02) |
| 6 | 01 | Repetition (1st or 2nd) |
| 7 | 12 | Actor number (even = female) |

### Emotion Codes

| Code | Emotion | Code | Emotion |
|------|---------|------|---------|
| 01 | Neutral | 05 | Angry |
| 02 | Calm | 06 | Fearful |
| 03 | Happy | 07 | Disgust |
| 04 | Sad | 08 | Surprised |

### Download

To download the dataset:
```bash
python src/utils/download_datasets.py
```

Or manually from: [RAVDESS on Zenodo](https://zenodo.org/record/1188976)

---

## Training Models

### Train on RAVDESS

```bash
python train_ravdess.py
```

### General Training

```bash
python train_model.py
```

Trained models are saved to the `models/` directory:
- `emotion_model.keras` / `emotion_model_best.keras` — CNN for spectrogram emotion classification
- `feature_scaler.joblib` — Feature normalization scaler
- `label_encoder.joblib` — Label encoder for emotion classes
- `class_map.json` — Emotion class mapping

---

## API Reference

The FastAPI backend exposes these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check & module status |
| `POST` | `/api/audio/analyze` | Analyze uploaded audio file |
| `GET` | `/api/entries?limit=50` | Get recent journal entries |
| `GET` | `/api/entries/range` | Query entries by date range |
| `POST` | `/api/entries/add` | Save a journal entry |
| `GET` | `/api/trends/burnout?days=30` | Burnout trend chart data |
| `GET` | `/api/trends/emotions?days=30` | Emotion distribution data |
| `GET` | `/api/insights?days=30` | AI-powered recommendations |

Interactive documentation available at `http://localhost:8000/docs` when the backend is running.

---

## Acoustic Features Explained

### Mel-Spectrogram
Visual representation of audio — x-axis is time, y-axis is frequency (Mel scale), color intensity is energy. Emotions create distinct patterns.

### Jitter
Variation in fundamental frequency period. Higher jitter → vocal fatigue, stress.

### Shimmer
Variation in amplitude between vocal cycles. High shimmer → hoarseness, fatigue, burnout.

### Pitch Features
- **Mean Pitch** — Average fundamental frequency
- **Pitch Std Dev** — Variability in pitch (lower = emotional flattening)
- **Pitch Range** — Max − min pitch

### MFCC (Mel-Frequency Cepstral Coefficients)
Compact representation of the spectral envelope — captures timbral qualities used by the CNN classifier.

---

## Burnout Score

```
Burnout Score = 0.25 × Jitter + 0.25 × Shimmer + 0.25 × PitchVariability + 0.25 × (1 − VoiceActivity)
```

| Range | Level |
|-------|-------|
| 0–25 | Healthy |
| 25–50 | Mild stress |
| 50–75 | Moderate burnout |
| 75–100 | Severe burnout |

---

## Privacy & Disclaimers

**Privacy:** All data stays on your device. No cloud uploads, no external servers. SQLite database is local.

**Disclaimer:** VocalVitals is a **research and educational tool** — it is NOT a substitute for professional medical or psychological evaluation. If you experience symptoms of depression, anxiety, or burnout, please contact a qualified mental health professional.

- [SAMHSA National Helpline](https://www.samhsa.gov/): 1-800-662-4357
- [Crisis Text Line](https://www.crisistextline.org/): Text HOME to 741741

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## References

```bibtex
@article{livingstone2018ravdess,
  title={The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)},
  author={Livingstone, Steven R and Russo, Frank A},
  journal={PLoS ONE},
  year={2018}
}
```

- Cummins et al. (2015) — Acoustic analysis of depression and burnout
- Schuller et al. (2013) — Emotion recognition from speech

---

**Made with care for mental health awareness**

*VocalVitals © 2026*
