"""Home page — landing / overview."""

import streamlit as st


def render():
    st.title("🎤 VocalVitals")
    st.markdown("### Your AI-Powered Speech Emotion & Burnout Tracker")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🎭 Emotion Detection")
            st.write(
                "Real-time emotion analysis from your voice. Detect emotional states "
                "including happiness, sadness, anger, and more."
            )

    with col2:
        with st.container(border=True):
            st.subheader("😞 Burnout Detection")
            st.write(
                "Identify burnout indicators through acoustic biomarkers like jitter, "
                "shimmer, and pitch variability."
            )

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("📔 Voice Journal")
            st.write(
                "Automatically track all your voice recordings with emotional and "
                "stress metadata for personal monitoring."
            )

    with col4:
        with st.container(border=True):
            st.subheader("📈 Trend Analysis")
            st.write(
                "Visualize your emotional and burnout patterns over time with "
                "interactive charts and insights."
            )

    st.write("")

    st.info(
        "**How It Works**\n\n"
        "VocalVitals analyzes your voice using advanced AI to detect emotions and burnout:\n\n"
        "1. Record or upload your voice (10-30 seconds)\n"
        "2. AI extracts acoustic features and emotional patterns\n"
        "3. Get instant results: emotion classification and burnout score\n"
        "4. Track trends over time with the voice journal"
    )

    st.warning(
        "**ℹ️ Disclaimer:** VocalVitals is a research and educational tool, "
        "NOT a medical device. It provides insights about emotional patterns but "
        "cannot diagnose mental health conditions. If experiencing burnout or "
        "mental health concerns, please consult with a healthcare professional."
    )
