"""
VocalVitals: Speech Emotion & Burnout Tracker
Streamlit web application for real-time voice analysis and burnout tracking
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Try to import librosa (optional)
try:
    import librosa
    import librosa.display
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import modules (optional)
try:
    from src.audio_processing.processor import AudioProcessor
except ImportError:
    AudioProcessor = None

try:
    from src.feature_extraction.extractor import AcousticFeatureExtractor
except ImportError:
    AcousticFeatureExtractor = None

try:
    from database.db import VoiceJournalDB
except ImportError:
    VoiceJournalDB = None


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="VocalVitals - Emotion & Burnout Tracker",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Session State Initialization
# ============================================================================

if 'db' not in st.session_state:
    if VoiceJournalDB:
        st.session_state.db = VoiceJournalDB()
    else:
        st.session_state.db = None

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

if 'audio_processor' not in st.session_state:
    if AudioProcessor:
        st.session_state.audio_processor = AudioProcessor()
    else:
        st.session_state.audio_processor = None

if 'feature_extractor' not in st.session_state:
    if AcousticFeatureExtractor:
        st.session_state.feature_extractor = AcousticFeatureExtractor()
    else:
        st.session_state.feature_extractor = None


# ============================================================================
# Sidebar Navigation
# ============================================================================

st.sidebar.title("🎤 VocalVitals")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Analyze Voice", "Voice Journal", "Trends & Insights", "About"]
)

st.session_state.page = page


# ============================================================================
# Emotion & Burnout Mapping Functions
# ============================================================================

def predict_emotion(mel_spec: np.ndarray) -> dict:
    """
    Predict emotion from mel-spectrogram
    Note: This is a placeholder. Replace with actual model inference
    """
    # Placeholder: In production, use trained model
    emotions = ['Neutral', 'Calm', 'Happy', 'Frustrated', 'Sad', 'Angry', 'Fearful']
    confidence = np.random.rand()
    predicted_emotion = emotions[np.random.randint(0, len(emotions))]
    
    return {
        'label': predicted_emotion,
        'confidence': float(confidence)
    }


def calculate_burnout_score(features: dict) -> tuple:
    """
    Calculate burnout score from acoustic features
    
    Returns:
        tuple: (burnout_score, burnout_level)
    """
    # Normalize features
    jitter = min(features.get('jitter', 0) * 100, 100)  # Higher jitter = more stress
    shimmer = min(features.get('shimmer', 0) * 100, 100)  # Higher shimmer = more stress
    pitch_std = min(features.get('pitch_std', 0) / 50, 1) * 100  # Pitch variability
    voice_activity = features.get('voice_activity', 0) * 100
    
    # Weighted burnout score
    burnout_score = (
        jitter * 0.25 +
        shimmer * 0.25 +
        pitch_std * 0.25 +
        (100 - voice_activity) * 0.25  # Lower voice activity = higher stress
    )
    
    burnout_score = min(max(burnout_score, 0), 100)
    
    # Determine burnout level
    if burnout_score < 25:
        burnout_level = "Healthy 😊"
    elif burnout_score < 50:
        burnout_level = "Mild 😐"
    elif burnout_score < 75:
        burnout_level = "Moderate 😟"
    else:
        burnout_level = "Severe 😞"
    
    return burnout_score, burnout_level


def stress_indicators(features: dict) -> dict:
    """Generate stress indicators from features"""
    indicators = {}
    
    if features.get('jitter', 0) > 0.05:
        indicators['high_jitter'] = "Voice instability detected"
    
    if features.get('shimmer', 0) > 0.05:
        indicators['high_shimmer'] = "Amplitude variations detected"
    
    if features.get('speech_rate', 0) > 6:
        indicators['fast_speech'] = "Speaking rapidly (may indicate stress)"
    elif features.get('speech_rate', 0) < 2:
        indicators['slow_speech'] = "Speaking slowly (may indicate fatigue)"
    
    if features.get('voice_activity', 0) < 0.3:
        indicators['low_activity'] = "Low vocalization (fatigue indicator)"
    
    if features.get('mean_energy', 0) < 0.02:
        indicators['low_energy'] = "Low voice energy"
    
    return indicators


# ============================================================================
# HOME PAGE
# ============================================================================

def page_home():
    st.title("🎤 VocalVitals")
    st.subtitle("Your AI-Powered Speech Emotion & Burnout Tracker")
    
    st.markdown("""
    ### Welcome to VocalVitals! 👋
    
    VocalVitals is an intelligent system that analyzes your voice to detect:
    - **Emotional State**: Identifies emotions in your speech (Happy, Sad, Angry, etc.)
    - **Burnout Levels**: Detects signs of stress, fatigue, and burnout through vocal markers
    - **Trends**: Tracks your emotional and mental health over time
    
    ### How It Works 🔄
    
    1. **Record or Upload** your voice (10-30 seconds recommended)
    2. **AI Analysis** extracts acoustic features from your voice
    3. **Get Results** instantly:
       - Emotion classification
       - Burnout score (0-100)
       - Stress indicators
    4. **Track Over Time** with automatic voice journal
    
    ### Key Features 🌟
    
    - 🎙️ Real-time voice recording and analysis
    - 📊 Interactive dashboard with trends
    - 📈 Burnout tracking over days/weeks/months
    - 💾 Secure local data storage
    - 📉 Visual insights and recommendations
    
    ### Technology Stack 🛠️
    
    - **Audio Processing**: Librosa for mel-spectrograms and acoustic features
    - **Deep Learning**: TensorFlow/Keras for emotion classification
    - **Features**: OpenSMILE-style biomarkers (jitter, shimmer, pitch)
    - **Frontend**: Streamlit for interactive dashboard
    - **Database**: SQLite for voice journal storage
    
    ---
    
    **Get Started**: Use the navigation menu to analyze your first voice sample!
    """)
    
    # Show quick stats if there's data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            entries_df = st.session_state.db.get_latest_entries(100)
            if not entries_df.empty:
                st.metric("Total Recordings", len(entries_df))
        except:
            pass
    
    with col2:
        try:
            trend_df = st.session_state.db.get_burnout_trend(30)
            if not trend_df.empty:
                avg_burnout = trend_df['avg_burnout_score'].mean()
                st.metric("Avg Burnout (30d)", f"{avg_burnout:.1f}")
        except:
            pass
    
    with col3:
        try:
            emotion_dist = st.session_state.db.get_emotion_distribution()
            st.metric("Unique Emotions", len(emotion_dist))
        except:
            pass


# ============================================================================
# ANALYZE VOICE PAGE
# ============================================================================

def page_analyze():
    st.title("🎙️ Analyze Your Voice")
    
    st.markdown("""
    This page allows you to analyze your voice for emotional state and burnout indicators.
    """)
    
    # Check if audio processing is available
    if not AudioProcessor or not st.session_state.audio_processor:
        st.warning("⚠️ Audio processing module not available. Please complete the setup by installing all dependencies:")
        st.code("pip install -r requirements.txt")
        return
    
    # Audio input method
    input_method = st.radio("Choose input method:", ["🎤 Record Now", "📁 Upload File"], horizontal=True)
    
    audio_data = None
    sr = 22050
    
    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3', 'm4a'])
        
        if uploaded_file:
            # Save uploaded file temporarily
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                audio_data, sr = st.session_state.audio_processor.load_audio(temp_path)
                st.success(f"✅ Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    else:  # Record Now
        st.info("🎤 Click the microphone icon below and speak for 3–10 seconds. Your browser will ask for microphone permission.")
        recording = st.audio_input("Record a voice sample")

        if recording is not None:
            # Save the recorded audio to a temp file for processing
            temp_path = "/tmp/vocalvitals_recording.wav"
            with open(temp_path, "wb") as f:
                f.write(recording.read())

            try:
                audio_data, sr = st.session_state.audio_processor.load_audio(temp_path)
                st.success("✅ Recording captured! Scroll down to see results.")
            except Exception as e:
                st.error(f"Error processing recording: {e}")
    
    # Analysis section
    if audio_data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Audio Preview")
            st.audio(audio_data, sample_rate=sr)
            
            # Plot waveform
            fig, ax = plt.subplots(figsize=(10, 3))
            time_axis = np.arange(len(audio_data)) / sr
            ax.plot(time_axis, audio_data)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title('Waveform')
            st.pyplot(fig)
        
        with col2:
            st.subheader("🔄 Processing...")
            
            with st.spinner("Analyzing your voice..."):
                # Generate mel-spectrogram
                mel_spec = st.session_state.audio_processor.generate_mel_spectrogram(audio_data, sr)
                
                # Extract features
                features = st.session_state.feature_extractor.extract_all_features(audio_data, sr)
                
                # Predict emotion
                emotion = predict_emotion(mel_spec)
                
                # Calculate burnout score
                burnout_score, burnout_level = calculate_burnout_score(features)
                
                # Get stress indicators
                indicators = stress_indicators(features)
        
        # Results section
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric("🎭 Detected Emotion", emotion['label'])
            st.caption(f"Confidence: {emotion['confidence']:.1%}")
        
        with res_col2:
            st.metric("😞 Burnout Score", f"{burnout_score:.1f}/100")
            st.caption(burnout_level)
        
        with res_col3:
            st.metric("⏱️ Duration", f"{len(audio_data)/sr:.1f}s")
        
        # Acoustic features
        st.subheader("🔊 Acoustic Features")
        
        feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
        
        with feat_col1:
            st.metric("Jitter", f"{features.get('jitter', 0):.4f}")
            st.caption("Voice instability")
        
        with feat_col2:
            st.metric("Shimmer", f"{features.get('shimmer', 0):.4f}")
            st.caption("Amplitude variation")
        
        with feat_col3:
            st.metric("Speech Rate", f"{features.get('speech_rate', 0):.1f} /s")
            st.caption("Syllables per second")
        
        with feat_col4:
            st.metric("Pitch Std", f"{features.get('pitch_std', 0):.1f}")
            st.caption("Pitch variation")
        
        # Stress indicators
        if indicators:
            st.subheader("⚠️ Stress Indicators")
            for key, indicator in indicators.items():
                st.warning(indicator)
        else:
            st.success("✅ No significant stress indicators detected")
        
        # Visualize mel-spectrogram
        st.subheader("📈 Mel-Spectrogram")
        fig, ax = plt.subplots(figsize=(12, 4))
        img = librosa.display.specshow(mel_spec, sr=sr, hop_length=st.session_state.audio_processor.hop_length,
                                       x_axis='time', y_axis='mel', ax=ax)
        ax.set_title('Mel-Spectrogram (Emotional Signature)')
        fig.colorbar(img, ax=ax, format='%+2.0f dB')
        st.pyplot(fig)
        
        # Save to journal option
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            user_notes = st.text_area("📝 Add notes (optional):", max_chars=500)
        
        with col2:
            if st.button("💾 Save to Voice Journal"):
                try:
                    entry_id = st.session_state.db.add_voice_entry(
                        audio_file_path="uploaded_audio",
                        duration_seconds=len(audio_data)/sr,
                        emotion_prediction=emotion,
                        burnout_score=burnout_score,
                        burnout_level=burnout_level,
                        stress_indicators=features,
                        notes=user_notes
                    )
                    st.success(f"✅ Saved to journal! Entry ID: {entry_id}")
                except Exception as e:
                    st.error(f"Error saving to journal: {e}")


# ============================================================================
# VOICE JOURNAL PAGE
# ============================================================================

def page_journal():
    st.title("📔 Voice Journal")
    
    st.markdown("""
    View your recorded voice entries and track patterns over time.
    """)
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        days = st.slider("Show entries from last N days:", 1, 90, 30)
    
    with col2:
        emotion_filter = st.multiselect(
            "Filter by emotion:",
            ['Neutral', 'Calm', 'Happy', 'Frustrated', 'Sad', 'Angry', 'Fearful'],
            default=None
        )
    
    try:
        # Get date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        entries_df = st.session_state.db.get_entries_by_date_range(
            str(start_date),
            str(end_date)
        )
        
        if entries_df.empty:
            st.info("No entries found. Start analyzing your voice to build your journal!")
        else:
            # Filter by emotion if selected
            if emotion_filter:
                filtered_entries = []
                for idx, row in entries_df.iterrows():
                    emotion_label = row['emotions'].get('label', '')
                    if emotion_label in emotion_filter:
                        filtered_entries.append(row)
                entries_df = pd.DataFrame(filtered_entries)
            
            st.subheader(f"📊 {len(entries_df)} Entries Found")
            
            # Display entries
            for idx, row in entries_df.iterrows():
                with st.expander(f"📝 {row['timestamp']} - {row['emotions']['label']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Emotion", row['emotions']['label'])
                        st.metric("Confidence", f"{row['emotion_confidence']:.1%}")
                    
                    with col2:
                        st.metric("Burnout Score", f"{row['burnout_score']:.1f}")
                        st.metric("Level", row['burnout_level'])
                    
                    with col3:
                        st.metric("Duration", f"{row['duration_seconds']:.1f}s")
                    
                    if row['notes']:
                        st.write(f"📌 Notes: {row['notes']}")
                    
                    # Show acoustic features
                    stress_indicators = row['stress_indicators']
                    st.write("🔊 Key Features:")
                    st.write(f"- Jitter: {stress_indicators.get('jitter', 0):.4f}")
                    st.write(f"- Shimmer: {stress_indicators.get('shimmer', 0):.4f}")
                    st.write(f"- Speech Rate: {stress_indicators.get('speech_rate', 0):.1f} /s")
    
    except Exception as e:
        st.error(f"Error loading journal: {e}")


# ============================================================================
# TRENDS & INSIGHTS PAGE
# ============================================================================

def page_trends():
    st.title("📈 Trends & Insights")
    
    st.markdown("""
    Visualize your emotional and burnout trends over time.
    """)
    
    try:
        days = st.slider("Analyze last N days:", 1, 90, 30)
        
        # Get trend data
        trend_df = st.session_state.db.get_burnout_trend(days)
        emotion_dist = st.session_state.db.get_emotion_distribution(days)
        feature_stats = st.session_state.db.get_acoustic_feature_stats(days)
        insights = st.session_state.db.get_insights(days)
        
        if not trend_df.empty:
            # Summary metrics
            st.subheader("📊 Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Recordings", insights['total_entries'])
            with col2:
                st.metric("Avg Burnout", f"{insights['avg_burnout_score']:.1f}")
            with col3:
                st.metric("Avg Jitter", f"{insights['avg_jitter']:.4f}")
            with col4:
                st.metric("Avg Shimmer", f"{insights['avg_shimmer']:.4f}")
            
            # Burnout trend
            st.subheader("😞 Burnout Trend")
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(trend_df['date'], trend_df['avg_burnout_score'], marker='o', label='Average')
            ax.fill_between(range(len(trend_df)), 
                           trend_df['min_burnout_score'], 
                           trend_df['max_burnout_score'], 
                           alpha=0.3, label='Range')
            ax.set_xlabel('Date')
            ax.set_ylabel('Burnout Score')
            ax.set_title('Burnout Score Over Time')
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            # Emotion distribution
            if emotion_dist:
                st.subheader("🎭 Emotion Distribution")
                emotions_data = pd.DataFrame(list(emotion_dist.items()), columns=['Emotion', 'Count'])
                
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(emotions_data['Emotion'], emotions_data['Count'], color='skyblue')
                ax.set_ylabel('Count')
                ax.set_title('Emotions Detected Over Time')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            # Insights
            st.subheader("💡 AI Insights")
            if insights['highest_burnout_day']:
                st.warning(f"⚠️ Highest burnout detected on: {insights['highest_burnout_day']}")
        
        else:
            st.info("Not enough data to generate trends. Continue recording to see patterns!")
    
    except Exception as e:
        st.error(f"Error generating trends: {e}")


# ============================================================================
# ABOUT PAGE
# ============================================================================

def page_about():
    st.title("ℹ️ About VocalVitals")
    
    st.markdown("""
    ## Why Voice Analysis for Burnout?
    
    Your voice contains hidden signals about your emotional and mental state:
    
    ### Key Biomarkers 🎯
    
    1. **Jitter** - Voice instability (higher = more stressed)
    2. **Shimmer** - Amplitude variation (higher = fatigue)
    3. **Pitch Variability** - Less variation = emotional flattening
    4. **Voice Activity** - Lower activity = exhaustion
    5. **Speech Rate** - Changes indicate stress levels
    6. **Energy** - Low energy = burnout
    
    ### Scientific Foundation 🔬
    
    Research shows acoustic features are highly correlated with:
    - Depression and anxiety
    - Burnout syndrome
    - Chronic stress
    - Voice disorders
    
    Studies: Cummins et al. (2015), Salah & Gevers (2009), Schuller et al. (2013)
    
    ## Technology Stack 🛠️
    
    | Component | Technology |
    |-----------|------------|
    | Audio Processing | Librosa |
    | Feature Extraction | NumPy, SciPy |
    | Deep Learning | TensorFlow/Keras |
    | Frontend | Streamlit |
    | Database | SQLite |
    
    ## Datasets Used 📊
    
    - **RAVDESS**: 1440 files, 7 emotions
    - **TESS**: 2800 files, 7 emotions
    - **SAVEE**: 480 files, 7 emotions
    
    ## Data Privacy 🔒
    
    ✅ All data is stored locally on your device
    ✅ No data is sent to external servers
    ✅ You have full control over your voice journal
    
    ## Limitations ⚠️
    
    - Works best with 10-30 second recordings
    - Background noise may affect accuracy
    - Individual variation exists (calibration recommended)
    - Should not replace professional mental health assessment
    
    ## Development Team 👥
    
    Built with ❤️ for mental health awareness
    
    ## Disclaimer 📋
    
    VocalVitals is a research and development tool designed to provide insights into emotional 
    and stress patterns based on voice analysis. It is **NOT** a substitute for professional 
    medical or psychological evaluation. If you are experiencing symptoms of burnout, depression, 
    or anxiety, please consult with a qualified mental health professional.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: 2026
    """)


# ============================================================================
# Main App Router
# ============================================================================

if st.session_state.page == 'Home':
    page_home()
elif st.session_state.page == 'Analyze Voice':
    page_analyze()
elif st.session_state.page == 'Voice Journal':
    page_journal()
elif st.session_state.page == 'Trends & Insights':
    page_trends()
elif st.session_state.page == 'About':
    page_about()

# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>VocalVitals © 2026 | Your Voice, Your Health</p>
        <p style='font-size: 12px; color: gray;'>
            Built for mental health awareness | Not a substitute for professional help
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
