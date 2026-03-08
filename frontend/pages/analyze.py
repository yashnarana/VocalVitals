"""Analyze page — upload audio and view emotion / burnout results."""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api_client import analyze_audio, save_entry


# ── Helpers ──────────────────────────────────────────────────────────
def _burnout_color(score: float) -> str:
    if score < 25:
        return "green"
    if score < 50:
        return "orange"
    if score < 75:
        return "orange"
    return "red"


def _burnout_emoji(level: str) -> str:
    return {"Healthy": "😊", "Mild": "😐", "Moderate": "😟", "Severe": "😞"}.get(level, "🤔")


# ── Page ─────────────────────────────────────────────────────────────
def render():
    st.title("🎙️ Analyze Your Voice")

    col_upload, col_results = st.columns(2)

    # ── Left column: upload & analyze ────────────────────────────────
    with col_upload:
        with st.container(border=True):
            st.subheader("Upload & Analyze")
            uploaded_file = st.file_uploader(
                "Select Audio File",
                type=["wav", "mp3", "m4a", "ogg"],
                help="Supported: WAV, MP3, M4A, OGG",
            )

            analyze_btn = st.button(
                "🔍 Analyze Voice",
                disabled=uploaded_file is None,
                use_container_width=True,
                type="primary",
            )

        if analyze_btn and uploaded_file is not None:
            with st.spinner("Analyzing..."):
                try:
                    result = analyze_audio(uploaded_file.read(), uploaded_file.name)
                    st.session_state["analysis_result"] = result
                    st.session_state["analysis_filename"] = uploaded_file.name
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    # ── Right column: results ────────────────────────────────────────
    result = st.session_state.get("analysis_result")

    with col_results:
        if result:
            with st.container(border=True):
                st.subheader("📊 Analysis Results")

                r1, r2 = st.columns(2)
                emotion = result["emotion"]
                burnout_score = result["burnout_score"]
                burnout_level = result["burnout_level"]

                with r1:
                    st.metric("Emotion", emotion["label"])
                    st.caption(f"{emotion['confidence']:.0f}% confidence")

                with r2:
                    st.metric(
                        "Burnout Score",
                        f"{burnout_score:.1f}/100",
                    )
                    st.caption(f"{_burnout_emoji(burnout_level)} {burnout_level}")

                st.progress(min(burnout_score / 100, 1.0))

                st.markdown("---")
                st.markdown("**🔊 Key Acoustic Features**")

                indicators = result.get("stress_indicators", {})
                f1, f2 = st.columns(2)
                with f1:
                    st.write(f"**Jitter:** {indicators.get('jitter', 0):.4f}")
                    st.write(f"**Speech Rate:** {indicators.get('speech_rate', 0):.1f} /s")
                with f2:
                    st.write(f"**Shimmer:** {indicators.get('shimmer', 0):.4f}")
                    st.write(f"**Mean Energy:** {indicators.get('mean_energy', 0):.4f}")

    # ── Save to journal ──────────────────────────────────────────────
    if result:
        with st.container(border=True):
            st.subheader("📝 Save to Voice Journal")
            user_notes = st.text_area(
                "Add Notes (Optional)",
                placeholder="How did you feel? Any observations?",
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Save to Journal", use_container_width=True):
                    try:
                        resp = save_entry(
                            filename=st.session_state.get("analysis_filename", "uploaded_audio"),
                            duration=3.0,
                            emotion_label=result["emotion"]["label"],
                            burnout_score=result["burnout_score"],
                            burnout_level=result["burnout_level"],
                            acoustic_features=result.get("stress_indicators", {}),
                            notes=user_notes,
                        )
                        st.success(f"✅ Saved to journal! Entry ID: {resp.get('id')}")
                    except Exception as exc:
                        st.error(f"Failed to save: {exc}")
            with c2:
                if st.button("🔄 New Analysis", use_container_width=True):
                    st.session_state.pop("analysis_result", None)
                    st.session_state.pop("analysis_filename", None)
                    st.rerun()
