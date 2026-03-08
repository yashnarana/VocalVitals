# VocalVitals Setup Instructions

## 🎯 Complete Installation & Usage Guide

This guide walks you through everything you need to use VocalVitals.

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (macOS)

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

**Time**: ~2-3 minutes depending on internet speed

### Step 2: Launch the App

```bash
streamlit run app/main.py
```

**Opens at**: `http://localhost:8501`

### Step 3: Analyze Your Voice!

1. Click "Analyze Voice" 
2. Upload a .wav, .mp3, or .m4a file
3. Get instant results:
   - Emotion (Happy, Sad, Angry, etc.)
   - Burnout Score (0-100)
   - Stress Indicators
   - Mel-Spectrogram visualization

---

## 📦 What You Got

### Core Modules

#### 1. Audio Processing (`src/audio_processing/processor.py`)
- Load audio files in any format
- Generate Mel-spectrograms
- Extract MFCC features
- Normalize audio data

**Usage**:
```python
from src.audio_processing import AudioProcessor

processor = AudioProcessor()
y, sr = processor.load_audio('audio.wav')
mel_spec = processor.generate_mel_spectrogram(y, sr)
```

#### 2. Feature Extraction (`src/feature_extraction/extractor.py`)
- **Jitter**: Voice instability (stress indicator)
- **Shimmer**: Amplitude variation (fatigue indicator)
- **Pitch**: Fundamental frequency & variability
- **Energy**: Loudness patterns
- **Speech Rate**: Speaking speed
- **MFCC**: Mel-Frequency Cepstral Coefficients

**Usage**:
```python
from src.feature_extraction import AcousticFeatureExtractor

extractor = AcousticFeatureExtractor()
features = extractor.extract_all_features(audio_time_series, sample_rate)
# Returns 40+ features in a dictionary
```

#### 3. Deep Learning Models (`src/models/emotion_models.py`)
- **EmotionCNN**: Convolutional Neural Network for Mel-spectrogram analysis
- **BurnoutClassifier**: Dense network for feature-based burnout detection
- **HybridEmotionModel**: Ensemble combining both approaches

**Usage**:
```python
from src.models import create_emotion_cnn, create_burnout_classifier

emotion_model = create_emotion_cnn(input_shape=(128, 128, 1), num_classes=7)
burnout_model = create_burnout_classifier(input_features=41, num_classes=4)
```

#### 4. Voice Journal Database (`database/db.py`)
- SQLite database for storing voice entries
- Automatic emotion & burnout tracking
- Trend analysis queries
- Privacy-first design (local storage only)

**Usage**:
```python
from database.db import VoiceJournalDB

db = VoiceJournalDB()
entry_id = db.add_voice_entry(
    audio_file_path="my_voice.wav",
    duration_seconds=3.5,
    emotion_prediction={'label': 'Happy', 'confidence': 0.85},
    burnout_score=35.0,
    burnout_level="Mild",
    stress_indicators={...}
)
```

#### 5. Streamlit Dashboard (`app/main.py`)
- Interactive web UI
- Real-time audio analysis
- Voice journal visualization
- Burnout trend charts
- Mobile-friendly design

---

## 🧠 Understanding the Technology

### Mel-Spectrograms: "Visual Sound"

```
Time →
Frequency
   ↓
   [Visual representation of sound]
   Darker = lower energy
   Brighter = higher energy
```

Different emotions create different patterns:
- **Happy**: Higher frequencies, more energy
- **Sad**: Lower frequencies, less consistent
- **Angry**: Sharp, irregular patterns

### Acoustic Biomarkers: "Voice Health Checkup"

| Metric | What It Means | Healthy Range | High = ? |
|--------|--------------|--------------|----------|
| Jitter | Voice vibration stability | <0.01 | Stress, fatigue |
| Shimmer | Amplitude variation | <0.05 | Voice fatigue |
| Pitch Std | Pitch variability | High = emotional | Low = depression |
| Energy | Voice loudness | Consistent | Low = burnout |
| Speech Rate | Words per minute | 3-5 /sec | High = anxiety |

### Model Architecture

```
Audio File
    ↓
[Librosa]
    ↓
Mel-Spectrogram (128×256)  +  Features (jitter, shimmer, etc.)
    ↓                            ↓
[CNN Model]                [Feature Classifier]
    ↓                            ↓
Emotion Softmax  +  Burnout Softmax
    ↓                            ↓
[Fusion Layer]
    ↓
Final Emotion Prediction (7 classes)
Emotion Confidence (0-1)
```

---

## 🎓 Using the Jupyter Notebook

The notebook guides you through the entire pipeline:

```bash
jupyter notebook notebooks/VocalVitals_Exploration.ipynb
```

**Sections**:
1. Import libraries
2. Load audio data
3. Generate Mel-spectrograms
4. Extract acoustic features
5. Build CNN model
6. Train model
7. Evaluate performance
8. Real-time prediction
9. Store data in database
10. Streamlit integration

**Run cells sequentially** to understand each step.

---

## 🚀 Training Your Own Models

### Option 1: Download Public Datasets

```bash
python src/utils/download_datasets.py
```

Downloads:
- **RAVDESS**: 1,440 files (Multiple actors, 7 emotions)
- **TESS**: 2,800 files (2 speakers, 7 emotions)
- **SAVEE**: 480 files (4 speakers, 7 emotions)

**Total size**: ~3GB
**Time**: 30 minutes to 2 hours

### Option 2: Use Your Own Data

Structure your data:
```
data/raw/
├── neutral/
│   ├── sample1.wav
│   └── sample2.wav
├── happy/
│   ├── sample1.wav
│   └── sample2.wav
└── sad/
    └── ...
```

### Option 3: Train via Script

```bash
python train_model.py
```

Customize training parameters in the script:
- Epochs (default: 100)
- Batch size (default: 32)
- Learning rate (0.001)
- Data split (80/20 train/val)

---

## 📊 Dashboard Features

### 1. Home Page
- Quick statistics
- Overview of system capabilities
- Feature overview

### 2. Analyze Voice
- Upload or record audio
- Visualize waveform
- Get instant emotion classification
- See detailed acoustic features
- Burnout score calculation
- Save to voice journal

### 3. Voice Journal
- Browse all past recordings
- Filter by emotion or date
- View detailed entry information
- Read your notes

### 4. Trends & Insights
- Burnout trend graph
- Emotion distribution pie chart
- Day-by-day comparisons
- AI-generated insights
- 7, 30, 90-day analysis

### 5. About
- Technology explanation
- Dataset information
- Privacy policy
- Disclaimer & resources

---

## 🔒 Privacy & Security

✅ **What VocalVitals Does**:
- Processes audio locally on your device
- Stores data in SQLite (local file)
- Never uploads to external servers
- No analytics or tracking
- No cloud storage by default

✅ **Your Data**:
- Remains on your device
- Fully under your control
- Can be deleted anytime
- No third-party access

---

## ❓ Troubleshooting

### Issue: "librosa not found"
```bash
pip install librosa
```

### Issue: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Issue: "Streamlit command not found"
```bash
pip install streamlit
```

### Issue: "Port 8501 already in use"
```bash
streamlit run app/main.py --server.port 8502
```

### Issue: Audio files not loading
- Check file format (.wav, .mp3, .m4a)
- Ensure FFmpeg installed: `brew install ffmpeg`
- Check file path is correct

### Issue: Model predictions not working
- Ensure model files exist in `models/` directory
- Check input shape matches model expectations
- Verify Mel-spectrogram shape (128×128)

---

## 🔬 Research & References

### Key Papers

1. **Emotion Recognition from Speech**
   - Schuller et al. (2013)
   - IEEE Transactions on Acoustics, Speech and Signal Processing

2. **Acoustic Markers of Burnout**
   - Cummins et al. (2015)
   - Proceedings of INTERSPEECH

3. **Deep Learning for Speech**
   - Hinton et al. (2012)
   - Neural Networks and various IEEE publications

### Tools & Libraries

- **Librosa**: Audio analysis library
  - Docs: https://librosa.org/
  - Citation: McVicar et al. (2015)

- **TensorFlow/Keras**: Deep learning framework
  - Docs: https://tensorflow.org/
  - Citation: Abadi et al. (2015)

- **Streamlit**: Web application framework
  - Docs: https://docs.streamlit.io/

---

## 🚀 Advanced Usage

### Custom Model Architecture

Edit `src/models/emotion_models.py`:
```python
def build_custom_model(input_shape):
    model = models.Sequential([
        # Add your custom layers
    ])
    return model
```

### Real-time Recording

Install PyAudio:
```bash
pip install pyaudio
```

Then use in your code:
```python
import sounddevice as sd
audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()
```

### Deploy to Cloud

Example for Heroku/AWS:
1. Create `Procfile`
2. Create `runtime.txt`
3. Deploy via cloud provider

---

## 📞 Support & Feedback

### Need Help?
- Check README.md for comprehensive docs
- Review notebook examples
- Examine source code comments
- Run example scripts

### Found a Bug?
- Describe the issue
- Include error message/traceback
- Specify OS and Python version
- Share reproduction steps

### Have Ideas?
- Suggest features via GitHub Issues
- Contribute code via Pull Requests
- Share research findings

---

## 📚 Learning Resources

### Audio Processing
- Course: "Audio Signal Processing for Music Applications" (Stanford)
- Course: "Music Signal Processing" (Coursera)
- Book: "Audio in Media" by Stanley Alten

### Deep Learning
- Course: "Deep Learning Specialization" (deeplearning.ai)
- Course: "Fast.ai" (practical deep learning)
- Research: "Deep Learning" (Goodfellow et al.)

### Speech Emotion Recognition
- Survey: "Emotion Recognition from Speech: A Review"
- Dataset: Zenodo emotion speech corpora
- Challenge: INTERSPEECH emotion recognition challenges

---

## ⚠️ Important Warnings

### Medical Disclaimer

🚨 **VocalVitals is NOT a medical device.**

It provides emotional insights from voice analysis but:
- Cannot diagnose mental health conditions
- Should not replace professional help
- Is for research and educational purposes only

**If you experience symptoms of:**
- Depression
- Anxiety
- Burnout
- Chronic stress

**Please contact:**
- Your healthcare provider
- Mental health professional
- Crisis hotline
  - SAMHSA: 1-800-662-4357
  - Crisis Text Line: Text HOME to 741741
  - National Suicide Prevention: 1-800-273-8255

---

## 🎯 Next Steps

1. **Try the Dashboard** → `streamlit run app/main.py`
2. **Record Your Voice** → Analyze Voice section
3. **Explore Trends** → Check Trends & Insights
4. **Download Datasets** → `python src/utils/download_datasets.py`
5. **Train Models** → `python train_model.py`
6. **Deploy App** → Follow cloud deployment guides

---

## 📄 License

VocalVitals is open source under the MIT License.
See LICENSE file for details.

---

**Made with ❤️ for mental health awareness**

*Version 1.0.0 - March 2026*
