# VocalVitals: Speech Emotion & Burnout Tracker

![VocalVitals](https://img.shields.io/badge/VocalVitals-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

An AI-powered system to detect emotional state and burnout indicators through voice analysis. VocalVitals combines deep learning, signal processing, and acoustic biomarkers to provide real-time insights into your mental health.

## 🎯 Features

- **🎤 Real-time Voice Analysis**: Upload or record your voice for instant emotion detection
- **😞 Burnout Detection**: Quantifies stress levels using acoustic biomarkers (jitter, shimmer, pitch variability)
- **📔 Voice Journal**: Automatically stores all recordings with emotional and stress metadata
- **📈 Trend Visualization**: Track emotional and burnout patterns over days/weeks/months
- **💡 AI-Powered Insights**: Get actionable recommendations based on your voice patterns
- **🔒 Privacy First**: All data stored locally - no cloud uploads
- **🧠 Hybrid Model**: Combines CNN analysis of spectrograms with acoustic feature classification

## 📊 How It Works

### The Voice-Health Connection

Your voice contains profound information about your emotional and mental state:

| Biomarker | Meaning | Burnout Signal |
|-----------|---------|----------------|
| **Jitter** | Frequency instability | ⬆️ Higher = More stressed |
| **Shimmer** | Amplitude variation | ⬆️ Higher = More fatigued |
| **Pitch Std Dev** | Pitch variability | ⬇️ Lower = Emotional flattening |
| **Voice Activity** | Speaking proportion | ⬇️ Lower = Exhaustion |
| **Speech Rate** | Syllables per second | Changes indicate stress |
| **Energy** | Voice loudness | ⬇️ Lower = Burnout |

### Analysis Pipeline

```
Audio Recording
    ↓
[Audio Processing] → Mel-Spectrogram (visual representation of sound)
    ↓
[Feature Extraction] → 40+ Acoustic Features (jitter, shimmer, energy, etc.)
    ↓
[CNN Spectrogram Classifier] + [Feature Classifier]
    ↓
[Emotion Predictions] + [Burnout Score]
    ↓
[Voice Journal Database]
    ↓
[Analytics & Insights Dashboard]
```

## 🛠 Technology Stack

### Core Machine Learning
- **TensorFlow/Keras**: Deep learning for emotion classification
- **PyTorch**: Alternative for Hugging Face transformer models
- **Scikit-learn**: Machine learning utilities

### Audio Processing
- **Librosa**: Mel-spectrogram generation and audio feature extraction
- **NumPy/SciPy**: Signal processing and mathematical operations
- **SoundDevice**: Real-time microphone recording

### Frontend & Data
- **Streamlit**: Interactive web dashboard
- **Pandas**: Data analysis and manipulation
- **SQLite**: Lightweight local database
- **Matplotlib/Seaborn**: Data visualization

### Development
- **Jupyter Notebook**: Exploratory data analysis and prototyping
- **Google Colab**: Free GPU computing (training)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- 2GB free disk space (for datasets)

### Step 1: Clone Repository

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# OR using conda
conda create -n vocalvitals python=3.10
conda activate vocalvitals
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Datasets (Optional, for training)

```bash
python src/utils/download_datasets.py
```

This downloads:
- **RAVDESS**: 1,440 speech files (7 emotions)
- **TESS**: 2,800 speech files (7 emotions)
- **SAVEE**: 480 speech files (7 emotions)

⚠️ Total size: ~3GB

## 🚀 Quick Start

### 1. Launch the Web App

```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

### 2. Analyze Your First Voice Sample

1. Go to "Analyze Voice" section
2. Upload an audio file (.wav, .mp3, .m4a) or record directly
3. Get instant results:
   - Emotion classification (Neutral, Happy, Sad, Angry, etc.)
   - Burnout score (0-100)
   - Stress biomarkers
   - Mel-spectrogram visualization

### 3. Track Your Trends

- Visit "Voice Journal" to see your history
- Check "Trends & Insights" for patterns over time
- Get recommendations based on your data

## 📚 Project Structure

```
VocalVitals/
├── app/
│   └── main.py                    # Streamlit dashboard application
├── src/
│   ├── audio_processing/
│   │   └── processor.py           # Audio loading, Mel-spectrogram generation
│   ├── feature_extraction/
│   │   └── extractor.py           # Jitter, shimmer, pitch, energy features
│   ├── models/
│   │   └── emotion_models.py      # CNN and burnout classifier models
│   └── utils/
│       └── download_datasets.py   # Dataset downloading utilities
├── database/
│   └── db.py                      # SQLite voice journal database
├── data/
│   ├── raw/                       # Raw audio files
│   └── processed/                 # Processed spectrograms
├── models/                        # Trained model weights
├── notebooks/                     # Jupyter notebooks for exploration
├── train_model.py                 # Model training script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔬 Training Your Own Models

### Step 1: Prepare Data

Organize audio files by emotion:
```
data/raw/
├── neutral/
│   ├── sample1.wav
│   └── sample2.wav
├── happy/
└── sad/
```

### Step 2: Train Models

```bash
python train_model.py
```

Models will be saved to `models/` directory:
- `emotion_cnn_final.h5`: CNN for spectrogram analysis
- `burnout_classifier_final.h5`: Feature-based burnout detector

### Step 3: Update Model Paths

Update `app/main.py` to load your trained models:

```python
from tensorflow.keras.models import load_model

emotion_model = load_model('models/emotion_cnn_final.h5')
burnout_model = load_model('models/burnout_classifier_final.h5')
```

## 📊 Datasets Used

### RAVDESS (Ryerson Audio-Visual Emotion Database)
- 24 professional actors
- 7 emotions: Neutral, Calm, Happy, Sad, Angry, Fearful, Surprised
- 1,440 speech files
- Download: [RAVDESS](https://zenodo.org/record/1188976)

### TESS (Toronto Emotional Speech Set)
- 2 female speakers
- 7 emotions per phrase
- 2,800 files
- Download: [TESS](https://tspace.library.utoronto.ca/handle/1807/24676)

### SAVEE (Surrey Audio-Visual Expressed Emotion)
- 4 male speakers
- 7 emotions
- 480 files
- Download: [SAVEE](http://kahlan.eps.surrey.ac.uk/savee/)

## 🔍 Feature Explanation

### Mel-Spectrogram
Visual representation of audio where:
- **X-axis**: Time
- **Y-axis**: Frequency (Mel scale - perceptually scaled)
- **Color intensity**: Energy at each time-frequency point

Emotions create distinct patterns - happy speech has higher frequencies, sad has lower.

### Jitter
Variation in fundamental frequency period. Higher jitter indicates:
- Vocal fatigue
- Stress
- Voice disorders

### Shimmer
Variation in amplitude between vocal cycles. High shimmer suggests:
- Hoarseness
- Fatigue
- Burnout

### Pitch Features
- **Mean Pitch**: Average fundamental frequency
- **Pitch Std Dev**: Variability in pitch
- **Pitch Range**: Max - min pitch

Lower variability can indicate emotional flattening (depression/burnout).

## 📈 Burnout Score Calculation

```
BurnoutScore = 0.25×Jitter + 0.25×Shimmer + 0.25×PitchVariability + 0.25×(1-VoiceActivity)

Score Range: 0-100
- 0-25: Healthy
- 25-50: Mild stress
- 50-75: Moderate burnout
- 75-100: Severe burnout
```

## 🎓 Research Background

VocalVitals is based on peer-reviewed research showing acoustic features correlate with:

- **Cummins et al. (2015)**: Acoustic analysis of depression and burnout
- **Schuller et al. (2013)**: Emotion recognition from speech
- **Salah & Gevers (2009)**: Audio-visual emotion database

Papers available at: [IEEE Xplore](https://ieeexplore.ieee.org/)

## 🔒 Privacy & Security

✅ **All data stays on your device**
- No cloud uploads
- No external servers
- SQLite database is local
- Encrypted at rest (optional)

## ⚠️ Limitations & Disclaimers

1. **Not a Diagnostic Tool**: VocalVitals provides insights, not medical diagnosis
2. **Background Noise**: Works best in quiet environments
3. **Individual Variation**: Calibration on your baseline is recommended
4. **Professional Help**: If experiencing burnout/depression, consult healthcare providers

## 🚨 Important Notice

**VocalVitals is a research and educational tool.** It is NOT a substitute for professional medical or psychological evaluation. 

If you experience symptoms of:
- Depression or anxiety
- Chronic stress
- Burnout syndrome

**Please contact a qualified mental health professional.**

Resources:
- [SAMHSA National Helpline](https://www.samhsa.gov/): 1-800-662-4357
- [Crisis Text Line](https://www.crisistextline.org/): Text HOME to 741741
- Your healthcare provider or therapist

## 💡 Future Enhancements

- [ ] Real-time microphone recording (WebRTC integration)
- [ ] Pre-trained models (download from Hugging Face)
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Integration with wearables (smartwatch)
- [ ] Advanced ML (Transformer models, Wav2Vec2)
- [ ] Export reports (PDF, CSV)
- [ ] Multi-user support with encryption
- [ ] Cloud sync (optional, encrypted)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or feedback:

- **GitHub Issues**: [VocalVitals Issues](https://github.com/yourname/vocalvitals/issues)
- **Email**: support@vocalvitals.example.com
- **Discord**: [VocalVitals Community](https://discord.gg/vocalvitals)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **RAVDESS Team**: For the comprehensive emotion database
- **Librosa Community**: For excellent audio processing library
- **TensorFlow Team**: For deep learning framework
- **Streamlit Team**: For making web apps simple
- **Research Community**: For emotion recognition publications

## 📖 References

```bibtex
@article{livingstone2018ravdess,
  title={The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)},
  author={Livingstone, Steven R and Russo, Frank A},
  journal={PLoS ONE},
  year={2018}
}

@dataset{tess,
  title={Toronto Emotional Speech Set (TESS)},
  author={Pichora-Fuller, M and Dupuis, K},
  organization={University of Toronto}
}

@inproceedings{schuller2013savee,
  title={The SAVEE Database},
  author={Haq, S and Jackson, P and Edge, J},
  conference={ACVR}
}
```

## 🌟 Star History

If you find VocalVitals helpful, please consider giving it a star ⭐

---

**Made with ❤️ for mental health awareness**

*VocalVitals © 2026*
