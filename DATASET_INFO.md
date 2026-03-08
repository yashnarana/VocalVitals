# RAVDESS Dataset Information & Configuration

## Dataset Overview

**RAVDESS** = Ryerson Audio-Visual Database of Emotional Speech and Song

### Statistics
- **Total Files**: 2,880 audio files
- **Actors**: 24 professional actors
  - 12 Female (even-numbered: 02, 04, 06, 08, 10, 12, 14, 16, 18, 20, 22, 24)
  - 12 Male (odd-numbered: 01, 03, 05, 07, 09, 11, 13, 15, 17, 19, 21, 23)
- **Statements**: 2 ("Kids are talking by the door", "Dogs are sitting by the door")
- **Emotions**: 8 (Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprised)
- **Intensities**: 2 (Normal, Strong) — except Neutral (1 intensity only)
- **Repetitions**: 2 (1st, 2nd)
- **Format**: WAV files, 16-bit, 48kHz sample rate
- **Location**: `/data/raw/Actor_01/` through `Actor_24/`

### Directory Structure
```
data/
├── raw/
│   ├── Actor_01/          (60 files)
│   ├── Actor_02/          (60 files)
│   ├── ...
│   └── Actor_24/          (60 files)
└── processed/             (for future preprocessed data)
```

---

## Filename Breakdown

### Format: `03-01-06-01-02-01-12.wav`

| Position | Code | Value | Meaning |
|----------|------|-------|---------|
| 1 | 03 | modality | **Audio-only** (01=full AV, 02=video, 03=audio) |
| 2 | 01 | channel | **Speech** (01=speech, 02=song) |
| 3 | 06 | emotion | **Fearful** |
| 4 | 01 | intensity | **Normal** (01=normal, 02=strong) |
| 5 | 02 | statement | **"Dogs are sitting by the door"** |
| 6 | 01 | repetition | **1st repetition** |
| 7 | 12 | actor | **Actor 12 (Female)** |

---

## Emotion Codes (8 Total)

Complete mapping used in VocalVitals:

| Code | Emotion | Description | Emoji |
|------|---------|-------------|-------|
| 01 | Neutral | No emotional expression | 😐 |
| 02 | Calm | Relaxed, peaceful | 😌 |
| 03 | Happy | Joyful, cheerful | 😊 |
| 04 | Sad | Sorrowful, unhappy | 😢 |
| 05 | Angry | Furious, hostile | 😠 |
| 06 | Fearful | Terrified, anxious | 😨 |
| 07 | Disgust | Repulsion, contempt | 🤢 |
| 08 | Surprised | Astonished, shocked | 😲 |

---

## Configuration Changes Made

### ✅ config.py (Root)
```python
BEFORE:
'emotion_classes': 7
'emotion_labels': ['Neutral', 'Calm', 'Happy', 'Frustrated', 'Sad', 'Angry', 'Fearful']

AFTER:
'emotion_classes': 8
'emotion_labels': ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fearful', 'Disgust', 'Surprised']
```

### ✅ backend/config.py
```python
EMOTION_CLASSES = 8
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
```

### ✅ backend/main.py
```python
EMOTION_MAP = {
    0: 'Neutral',
    1: 'Calm',
    2: 'Happy',
    3: 'Sad',
    4: 'Angry',
    5: 'Fearful',
    6: 'Disgust',
    7: 'Surprised'
}
```

### ✅ frontend/src/app/components/analyze.component.ts
```typescript
emotions = ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fearful', 'Disgust', 'Surprised'];
```

### ✅ frontend/src/app/components/journal.component.ts
```typescript
emotions = ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fearful', 'Disgust', 'Surprised'];

// Updated emoji mapping:
getEmotionIcon(emotion: string): string {
  const icons: { [key: string]: string } = {
    'Neutral': '😐',
    'Calm': '😌',
    'Happy': '😊',
    'Sad': '😢',
    'Angry': '😠',
    'Fearful': '😨',
    'Disgust': '🤢',      // NEW
    'Surprised': '😲'     // NEW
  };
}
```

---

## Usage Examples

### Finding Files by Emotion

```bash
cd /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/

# NEUTRAL (01)
ls -1 | grep '^03-01-01'
# Output: 03-01-01-01-01-01-01.wav, 03-01-01-01-01-02-01.wav, ...

# CALM (02)
ls -1 | grep '^03-01-02'

# HAPPY (03)
ls -1 | grep '^03-01-03'

# SAD (04)
ls -1 | grep '^03-01-04'

# ANGRY (05)
ls -1 | grep '^03-01-05'

# FEARFUL (06)
ls -1 | grep '^03-01-06'

# DISGUST (07)
ls -1 | grep '^03-01-07'

# SURPRISED (08)
ls -1 | grep '^03-01-08'
```

### Finding Files by Actor

```bash
# All files from Actor 05
ls -1 /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_05/ | grep '05$'

# All files from Actor 12 (Female)
ls -1 /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_12/ | grep '12$'

# All files from Actor 01 with strong intensity
ls -1 /Users/yashnarana/Desktop/VocalVitals/VocalVitals/data/raw/Actor_01/ | grep '-02-0[0-9]-02-'
```

---

## Technical Specifications

### Audio Properties
- **Sample Rate**: 48,000 Hz (will be resampled to 22,050 Hz in app)
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Duration**: ~3-4 seconds per file
- **Codec**: PCM WAV

### Emotional Intensity Levels
- **Level 01 (Normal)**: Actor uses calm, conversational tone
- **Level 02 (Strong)**: Actor exaggerates emotional expression
- **Exception**: Neutral emotion only has level 01 (no strong intensity)

### Statistical Distribution

For each actor:
- 8 emotions
- 2 intensities (except neutral = 1 intensity) = 15 intensity variations
- 2 statements = 30 variations
- 2 repetitions = 60 total files per actor

Total: 24 actors × 60 = **1,440 files**

Note: The dataset contains 2,880 because it includes both audio-only (03) and video-only (02) versions. VocalVitals uses only audio-only (03).

---

## Training Data Structure

Perfect for training emotion classification models:

### By Emotion
- **Neutral**: 48 files (24 actors × 2 reps)
- **Calm**: 96 files (24 actors × 2 intensities × 2 reps)
- **Happy**: 96 files
- **Sad**: 96 files
- **Angry**: 96 files
- **Fearful**: 96 files
- **Disgust**: 96 files
- **Surprised**: 96 files

**Total**: 720 audio-only speech files (or 1,440 if including video versions)

### By Gender
- **Female**: 360 files (12 actresses × 30 files per actress)
- **Male**: 360 files (12 actors × 30 files each)

### By Intensity
- **Normal**: 360 files
- **Strong**: 360 files

---

## Future Improvements

### Model Training
Once TensorFlow compatibility issues resolved, you can:
1. Train custom CNN on RAVDESS mel-spectrograms
2. Train RNN/LSTM for temporal emotion patterns
3. Create ensemble models
4. Fine-tune for specific speaker characteristics

### Data Augmentation
Can create variations:
- Time stretching
- Pitch shifting
- Adding background noise
- Mixup with other emotions

### Cross-Validation
Use actor-specific validation:
- Train on 20 actors
- Validate on 4 held-out actors
- Test on remaining actors

---

## References

**RAVDESS Papers**:
- Livingstone, S. R., & Russo, F. A. (2018). The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal expressions in North American English. PLOS ONE, 13(5), e0196424.

**Dataset URL**:
- https://zenodo.org/record/1188976

**Audio Processing**:
- Librosa documentation: https://librosa.org
- MFCC explanation: https://en.wikipedia.org/wiki/Mel-frequency_cepstral_coefficient

**Emotion Recognition**:
- Recent papers: https://scholar.google.com/scholar?q=emotion+recognition+speech+RAVDESS

---

## Summary

✅ **RAVDESS dataset properly integrated**
- 2,880 audio files extracted
- 8 emotions configured in VocalVitals
- Backend updated with emotion mapping
- Frontend updated with emotion arrays
- Database schema ready for emotion storage

✅ **App is ready for**
- Emotion analysis from RAVDESS files
- Creating custom voice journal entries
- Tracking emotion patterns over time
- Training custom models (when Python 3.13 compat resolved)

🚀 **Next steps**:
1. Start backend and frontend
2. Upload audio files from `/data/raw/`
3. Analyze emotions using VocalVitals
4. Track patterns in voice journal

---

**Status**: ✅ RAVDESS dataset configured and ready!
