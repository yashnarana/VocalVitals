"""Trends & Insights page — charts for burnout trend and emotion distribution."""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api_client import get_burnout_trend, get_emotion_distribution, get_insights

import pandas as pd


def render():
    st.title("📈 Trends & Insights")

    days = st.selectbox(
        "Time Period",
        options=[7, 14, 30, 90],
        format_func=lambda d: f"Last {d} Days",
        index=2,
    )

    # ── Fetch data ───────────────────────────────────────────────────
    trends = []
    emotion_dist = {}
    insights_data = None

    try:
        with st.spinner("Loading trends..."):
            trends = get_burnout_trend(days)
            emotion_dist = get_emotion_distribution(days)
            insights_data = get_insights(days)
    except Exception as exc:
        st.error(f"Failed to load trends: {exc}")

    # ── Burnout Trend Chart ──────────────────────────────────────────
    if trends:
        with st.container(border=True):
            st.subheader("📊 Burnout Trend")

            df = pd.DataFrame(trends)
            if "date" in df.columns and "avg_burnout" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")
                st.line_chart(df[["avg_burnout"]], y_label="Burnout Score", color="#dc3545")
            elif "date" in df.columns and "avg_burnout_score" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date")
                st.line_chart(df[["avg_burnout_score"]], y_label="Burnout Score", color="#dc3545")
            else:
                st.dataframe(df)

            # Summary cards
            if len(trends) > 0:
                cols = st.columns(min(len(trends), 6))
                for i, trend in enumerate(trends[: len(cols)]):
                    with cols[i]:
                        date_label = trend.get("date", "")
                        score = trend.get("avg_burnout", trend.get("avg_burnout_score", 0))
                        st.metric(date_label, f"{score:.0f}")

    # ── Emotion Distribution Chart ───────────────────────────────────
    if emotion_dist:
        with st.container(border=True):
            st.subheader("😊 Emotion Distribution")

            df_emo = pd.DataFrame(
                {"Emotion": list(emotion_dist.keys()), "Count": list(emotion_dist.values())}
            )
            st.bar_chart(df_emo.set_index("Emotion"), y_label="Count")

    # ── Insights ─────────────────────────────────────────────────────
    if insights_data:
        with st.container(border=True):
            st.subheader("💡 AI Insights")

            ic1, ic2 = st.columns(2)

            patterns = insights_data.get("key_patterns", [])
            recommendations = insights_data.get("recommendations", [])
            strengths = insights_data.get("strengths", [])
            concerns = insights_data.get("concerns", [])

            with ic1:
                if patterns:
                    st.markdown("**🎯 Key Patterns**")
                    for p in patterns:
                        st.write(f"- {p}")
                if strengths:
                    st.markdown("**💪 Strengths**")
                    for s in strengths:
                        st.write(f"- {s}")

            with ic2:
                if recommendations:
                    st.markdown("**💡 Recommendations**")
                    for r in recommendations:
                        st.write(f"- {r}")
                if concerns:
                    st.markdown("**⚠️ Concerns**")
                    for c in concerns:
                        st.write(f"- {c}")

            overall = insights_data.get("overall_assessment")
            if overall:
                st.markdown("---")
                st.markdown("**📋 Overall Assessment**")
                st.write(overall)

            # Show summary stats if present
            avg_burnout = insights_data.get("avg_burnout_score")
            total = insights_data.get("total_entries")
            if avg_burnout is not None or total is not None:
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                if avg_burnout is not None:
                    m1.metric("Avg Burnout", f"{avg_burnout:.1f}")
                if total is not None:
                    m2.metric("Total Entries", total)
                avg_jitter = insights_data.get("avg_jitter")
                if avg_jitter is not None:
                    m3.metric("Avg Jitter", f"{avg_jitter:.4f}")
