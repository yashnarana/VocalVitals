"""About page — project info, tech stack, how-it-works, privacy."""

import streamlit as st
from datetime import datetime


def render():
    st.title("ℹ️ About VocalVitals")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ── Mission ──────────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("🎯 Our Mission")
            st.write(
                "VocalVitals is an innovative platform that uses artificial intelligence "
                "and acoustic analysis to detect emotional state and burnout risk through "
                "voice analysis. We believe that early detection of burnout can help prevent "
                "serious health complications and improve overall wellbeing."
            )

        # ── Technology Stack ─────────────────────────────────────────
        with st.container(border=True):
            st.subheader("🛠️ Technology Stack")
            tc1, tc2 = st.columns(2)
            with tc1:
                st.markdown("**Frontend**")
                st.write("✅ Streamlit (Python)")
                st.write("✅ Plotly / Matplotlib")
                st.write("✅ Pandas")
            with tc2:
                st.markdown("**Backend**")
                st.write("✅ FastAPI (Python)")
                st.write("✅ Librosa (Audio)")
                st.write("✅ SciPy / NumPy")
                st.write("✅ SQLite")

        # ── How It Works ─────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("🔊 How It Works")
            st.markdown(
                "1. **Record or Upload:** Provide an audio sample of your voice (any language, 5+ seconds)\n"
                "2. **Audio Analysis:** Extract acoustic features like pitch, jitter, shimmer, and speech rate\n"
                "3. **Emotion Detection:** ML model classifies emotional state (7 emotions)\n"
                "4. **Burnout Assessment:** Calculate burnout risk score (0-100) based on acoustic biomarkers\n"
                "5. **Journal & Track:** Store entries and monitor trends over time\n"
                "6. **Get Insights:** Receive personalized recommendations based on your patterns"
            )

        # ── Acoustic Features ────────────────────────────────────────
        with st.container(border=True):
            st.subheader("📊 Acoustic Features Analyzed")
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                st.markdown("**Pitch & Frequency**")
                st.write("• Mean Pitch (Hz)")
                st.write("• F0 Contour")
                st.write("• Vibrato Rate")
            with ac2:
                st.markdown("**Voice Quality**")
                st.write("• Jitter (%)")
                st.write("• Shimmer (dB)")
                st.write("• HNR Ratio")
            with ac3:
                st.markdown("**Speech Patterns**")
                st.write("• Speech Rate")
                st.write("• Energy Level")
                st.write("• MFCC Coefficients")

        # ── Privacy ──────────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("⚖️ Privacy & Data")
            st.markdown("**Your privacy is our priority.**")
            st.write("✅ Audio files are processed locally/securely")
            st.write("✅ Only acoustic features are stored (not raw audio)")
            st.write("✅ Your data remains in your local SQLite database")
            st.write("✅ No data is sent to external servers")
            st.write("✅ You can delete entries at any time")

        # ── Disclaimer ───────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("⚠️ Disclaimer")
            st.write(
                "**VocalVitals is for informational purposes only.** "
                "This application is not a medical device and should not be used for "
                "diagnosis or treatment of medical conditions. The emotion and burnout "
                "assessments are based on voice analysis patterns and should not replace "
                "professional medical advice. If you suspect you have burnout, anxiety, "
                "depression, or other mental health concerns, please consult with a "
                "qualified healthcare professional."
            )

        # ── References ───────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("📚 References")
            st.write("• Schuller, B., et al. (2019). The INTERSPEECH 2019 Computational Paralinguistics Challenge")
            st.write("• Cummins, N., et al. (2017). Speech Analysis for Health: Current Status and Prospects")
            st.write("• Librosa: Audio and music signal analysis library")

    with col_side:
        # ── Quick Links ──────────────────────────────────────────────
        with st.container(border=True):
            st.subheader("📱 Quick Links")
            st.page_link("app.py", label="🏠 Home")
            st.write("🎙️ Analyze Voice — select *Analyze* in sidebar")
            st.write("📔 Voice Journal — select *Journal* in sidebar")
            st.write("📈 Trends — select *Trends* in sidebar")

        st.info(
            "**😊 Did You Know?**\n\n"
            "Voice changes are one of the earliest indicators of burnout. "
            "Stressed individuals often show increased jitter and shimmer in their voice!"
        )

        st.success(
            "**🎯 Get Started**\n\n"
            "Start analyzing your voice today to track your emotional wellbeing "
            "and monitor burnout risk over time."
        )

    st.markdown("---")
    st.markdown(
        f"<center>&copy; {datetime.now().year} VocalVitals. All rights reserved.</center>",
        unsafe_allow_html=True,
    )
