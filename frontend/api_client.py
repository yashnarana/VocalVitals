"""
API client for the VocalVitals FastAPI backend.
"""

import requests
from typing import Optional

API_BASE = "http://localhost:8000/api"


def analyze_audio(file_bytes: bytes, filename: str) -> dict:
    """Upload an audio file and get emotion / burnout analysis."""
    files = {"file": (filename, file_bytes)}
    resp = requests.post(f"{API_BASE}/audio/analyze", files=files, timeout=60)
    resp.raise_for_status()
    return resp.json()


def get_entries(limit: int = 100) -> list:
    """Fetch recent voice journal entries."""
    resp = requests.get(f"{API_BASE}/entries", params={"limit": limit}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_entries_by_range(start_date: str, end_date: str) -> list:
    """Fetch entries within a date range (YYYY-MM-DD)."""
    resp = requests.get(
        f"{API_BASE}/entries/range",
        params={"start_date": start_date, "end_date": end_date},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def save_entry(
    filename: str,
    duration: float,
    emotion_label: str,
    burnout_score: float,
    burnout_level: str,
    acoustic_features: dict,
    notes: str = "",
) -> dict:
    """Save an analysis result to the voice journal."""
    resp = requests.post(
        f"{API_BASE}/entries/add",
        params={
            "filename": filename,
            "duration": duration,
            "emotion_label": emotion_label,
            "burnout_score": burnout_score,
            "burnout_level": burnout_level,
            "notes": notes,
        },
        json=acoustic_features,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def get_burnout_trend(days: int = 30) -> list:
    """Get burnout score trend over the given number of days."""
    resp = requests.get(f"{API_BASE}/trends/burnout", params={"days": days}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_emotion_distribution(days: int = 30) -> dict:
    """Get emotion distribution counts."""
    resp = requests.get(f"{API_BASE}/trends/emotions", params={"days": days}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_insights(days: int = 30) -> dict:
    """Get AI-generated insights and recommendations."""
    resp = requests.get(f"{API_BASE}/insights", params={"days": days}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def health_check() -> Optional[dict]:
    """Check if the backend is reachable."""
    try:
        resp = requests.get("http://localhost:8000/api/health", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None
