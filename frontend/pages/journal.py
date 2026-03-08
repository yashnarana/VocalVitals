"""Voice Journal page — browse, filter, and manage past entries."""

import streamlit as st
import sys, os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api_client import get_entries


EMOTIONS = ["Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"]

EMOTION_ICONS = {
    "Neutral": "😐",
    "Calm": "😌",
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😠",
    "Fearful": "😨",
    "Disgust": "🤢",
    "Surprised": "😲",
}

PAGE_SIZE = 10


def _burnout_badge(score: float) -> str:
    if score < 25:
        return "🟢"
    if score < 50:
        return "🟡"
    if score < 75:
        return "🟠"
    return "🔴"


def render():
    st.title("📔 Voice Journal")

    # ── Filters ──────────────────────────────────────────────────────
    with st.container(border=True):
        st.subheader("🔍 Filter Entries")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            selected_emotion = st.selectbox("Emotion", ["All Emotions"] + EMOTIONS)
        with fc2:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=90))
        with fc3:
            end_date = st.date_input("End Date", value=datetime.now().date())

        bc1, bc2 = st.columns([1, 1])
        with bc1:
            refresh = st.button("🔄 Refresh")
        with bc2:
            clear = st.button("↻ Clear Filters")

    if clear:
        st.rerun()

    # ── Load entries ─────────────────────────────────────────────────
    if "journal_entries" not in st.session_state or refresh:
        try:
            with st.spinner("Loading entries..."):
                st.session_state["journal_entries"] = get_entries(limit=100)
        except Exception as exc:
            st.error(f"Failed to load entries: {exc}")
            st.session_state["journal_entries"] = []

    entries = st.session_state.get("journal_entries", [])

    # ── Apply filters ────────────────────────────────────────────────
    filtered = entries
    if selected_emotion != "All Emotions":
        filtered = [e for e in filtered if e.get("emotion_label") == selected_emotion]

    if start_date and end_date:
        filtered = [
            e
            for e in filtered
            if start_date <= datetime.fromisoformat(e.get("timestamp", "2000-01-01")).date() <= end_date
        ]

    if not filtered:
        st.info("No entries found. Start by **Analyzing your voice**!")
        return

    # ── Pagination ───────────────────────────────────────────────────
    total_pages = max(1, -(-len(filtered) // PAGE_SIZE))  # ceil division
    page = st.session_state.get("journal_page", 1)
    page = min(page, total_pages)

    page_entries = filtered[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]

    # ── Display entries ──────────────────────────────────────────────
    for entry in page_entries:
        emotion_label = entry.get("emotion_label", "Unknown")
        icon = EMOTION_ICONS.get(emotion_label, "🤔")
        burnout = entry.get("burnout_score", 0)
        badge = _burnout_badge(burnout)

        with st.container(border=True):
            h1, h2, h3 = st.columns([1, 4, 2])
            with h1:
                st.markdown(f"## {icon}")
            with h2:
                st.markdown(f"**{emotion_label}**")
                st.caption(entry.get("timestamp", ""))
            with h3:
                st.markdown(f"{badge} Burnout: **{burnout:.0f}**")

            # Acoustic features
            features = entry.get("acoustic_features", {})
            if features:
                af1, af2 = st.columns(2)
                with af1:
                    st.write(f"**Duration:** {entry.get('duration_seconds', 0):.2f}s")
                    st.write(f"**Jitter:** {features.get('jitter', 0):.4f}")
                    st.write(f"**Shimmer:** {features.get('shimmer', 0):.4f}")
                with af2:
                    st.write(f"**Pitch (Hz):** {features.get('mean_pitch', 0):.1f}")
                    st.write(f"**Energy:** {features.get('mean_energy', 0):.4f}")
                    st.write(f"**Speech Rate:** {features.get('speech_rate', 0):.1f}/s")

            notes = entry.get("notes")
            if notes:
                st.markdown(f"📝 **Notes:** {notes}")

    # ── Pagination controls ──────────────────────────────────────────
    if total_pages > 1:
        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.button("⬅ Previous", disabled=page <= 1):
                st.session_state["journal_page"] = page - 1
                st.rerun()
        with p2:
            st.markdown(f"<center>Page {page} of {total_pages}</center>", unsafe_allow_html=True)
        with p3:
            if st.button("Next ➡", disabled=page >= total_pages):
                st.session_state["journal_page"] = page + 1
                st.rerun()
