"""
VocalVitals - Streamlit Frontend
AI-Powered Speech Emotion & Burnout Tracker
"""

import streamlit as st

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="VocalVitals",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)

from pages import home, analyze, journal, trends, about

# ── Sidebar Navigation ──────────────────────────────────────────────
st.sidebar.markdown("## 🎤 **VocalVitals**")
st.sidebar.caption("Your Voice, Your Health")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Analyze", "Journal", "Trends", "About"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small>VocalVitals © 2026<br>Built for mental health awareness<br>"
    "Not a substitute for professional help</small>",
    unsafe_allow_html=True,
)

# ── Page Router ──────────────────────────────────────────────────────
if page == "Home":
    home.render()
elif page == "Analyze":
    analyze.render()
elif page == "Journal":
    journal.render()
elif page == "Trends":
    trends.render()
elif page == "About":
    about.render()
