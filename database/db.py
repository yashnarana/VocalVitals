"""
Database Module for Voice Journal
SQLite database to track emotion and burnout trends over time
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class VoiceJournalDB:
    """SQLite database for voice journal entries"""
    
    def __init__(self, db_path: str = "database/voice_journal.db"):
        """
        Initialize database connection
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Voice entries table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                audio_file_path TEXT,
                duration_seconds REAL,
                emotions TEXT,
                emotion_confidence REAL,
                burnout_score REAL,
                burnout_level TEXT,
                stress_indicators TEXT,
                notes TEXT
            )
        ''')
        
        # Acoustic features table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS acoustic_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voice_entry_id INTEGER,
                jitter REAL,
                shimmer REAL,
                voice_activity REAL,
                speech_rate REAL,
                mean_pitch REAL,
                pitch_std REAL,
                mean_energy REAL,
                energy_std REAL,
                spectral_centroid_mean REAL,
                zero_crossing_rate_mean REAL,
                FOREIGN KEY(voice_entry_id) REFERENCES voice_entries(id)
            )
        ''')
        
        # Daily summary table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                avg_burnout_score REAL,
                max_stress_level TEXT,
                num_entries INTEGER,
                overall_mood TEXT,
                insights TEXT
            )
        ''')
        
        self.conn.commit()
    
    def add_voice_entry(self, 
                       audio_file_path: str,
                       duration_seconds: float,
                       emotion_prediction: Dict,
                       burnout_score: float,
                       burnout_level: str,
                       stress_indicators: Dict,
                       notes: str = "") -> int:
        """
        Add a new voice entry to the database
        
        Args:
            audio_file_path (str): Path to audio file
            duration_seconds (float): Duration of recording
            emotion_prediction (dict): Emotion label and confidence
            burnout_score (float): Burnout score (0-100)
            burnout_level (str): Burnout level (healthy, mild, moderate, severe)
            stress_indicators (dict): Dictionary of acoustic features
            notes (str): User notes
        
        Returns:
            int: ID of new entry
        """
        emotions_json = json.dumps(emotion_prediction)
        stress_json = json.dumps(stress_indicators)
        
        self.cursor.execute('''
            INSERT INTO voice_entries 
            (audio_file_path, duration_seconds, emotions, emotion_confidence, 
             burnout_score, burnout_level, stress_indicators, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            audio_file_path, 
            duration_seconds,
            emotions_json,
            emotion_prediction.get('confidence', 0),
            burnout_score,
            burnout_level,
            stress_json,
            notes
        ))
        
        entry_id = self.cursor.lastrowid
        self.conn.commit()
        
        # Add acoustic features
        self.add_acoustic_features(entry_id, stress_indicators)
        
        return entry_id
    
    def add_acoustic_features(self, voice_entry_id: int, features: Dict):
        """
        Add acoustic features for a voice entry
        
        Args:
            voice_entry_id (int): ID of voice entry
            features (dict): Dictionary of acoustic features
        """
        self.cursor.execute('''
            INSERT INTO acoustic_features 
            (voice_entry_id, jitter, shimmer, voice_activity, speech_rate,
             mean_pitch, pitch_std, mean_energy, energy_std,
             spectral_centroid_mean, zero_crossing_rate_mean)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            voice_entry_id,
            features.get('jitter', 0),
            features.get('shimmer', 0),
            features.get('voice_activity', 0),
            features.get('speech_rate', 0),
            features.get('mean_pitch', 0),
            features.get('pitch_std', 0),
            features.get('mean_energy', 0),
            features.get('energy_std', 0),
            features.get('spectral_centroid_mean', 0),
            features.get('zero_crossing_rate_mean', 0)
        ))
        
        self.conn.commit()
    
    def get_entries_by_date_range(self, 
                                  start_date: str,
                                  end_date: str) -> pd.DataFrame:
        """
        Get voice entries within date range
        
        Args:
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)
        
        Returns:
            pd.DataFrame: Entries in date range
        """
        query = '''
            SELECT * FROM voice_entries
            WHERE DATE(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, self.conn, params=(start_date, end_date))
        
        # Parse JSON columns
        if not df.empty:
            df['emotions'] = df['emotions'].apply(json.loads)
            df['stress_indicators'] = df['stress_indicators'].apply(json.loads)
        
        return df
    
    def get_latest_entries(self, limit: int = 10) -> pd.DataFrame:
        """
        Get latest voice entries
        
        Args:
            limit (int): Number of entries to retrieve
        
        Returns:
            pd.DataFrame: Latest entries
        """
        query = '''
            SELECT * FROM voice_entries
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, self.conn, params=(limit,))
        
        if not df.empty:
            df['emotions'] = df['emotions'].apply(json.loads)
            df['stress_indicators'] = df['stress_indicators'].apply(json.loads)
        
        return df
    
    def get_burnout_trend(self, days: int = 30) -> pd.DataFrame:
        """
        Get burnout score trend over last N days
        
        Args:
            days (int): Number of days to look back
        
        Returns:
            pd.DataFrame: Burnout trend data
        """
        query = '''
            SELECT 
                DATE(timestamp) as date,
                AVG(burnout_score) as avg_burnout_score,
                MAX(burnout_score) as max_burnout_score,
                MIN(burnout_score) as min_burnout_score,
                COUNT(*) as num_entries
            FROM voice_entries
            WHERE timestamp > datetime('now', '-' || ? || ' days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        '''
        
        df = pd.read_sql_query(query, self.conn, params=(days,))
        return df
    
    def get_emotion_distribution(self, days: int = 30) -> Dict:
        """
        Get emotion distribution over last N days
        
        Args:
            days (int): Number of days to look back
        
        Returns:
            dict: Emotion distribution
        """
        df = self.get_entries_by_date_range(
            datetime.fromtimestamp(0).strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d')
        )
        
        if df.empty:
            return {}
        
        # Extract emotions from JSON column
        emotion_counts = {}
        for emotions_json in df['emotions']:
            emotion = emotions_json.get('label', 'unknown')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return emotion_counts
    
    def get_acoustic_feature_stats(self, days: int = 30) -> pd.DataFrame:
        """
        Get acoustic feature statistics over last N days
        
        Args:
            days (int): Number of days to look back
        
        Returns:
            pd.DataFrame: Feature statistics
        """
        query = '''
            SELECT 
                AVG(jitter) as avg_jitter,
                AVG(shimmer) as avg_shimmer,
                AVG(voice_activity) as avg_voice_activity,
                AVG(speech_rate) as avg_speech_rate,
                AVG(mean_pitch) as avg_pitch,
                AVG(mean_energy) as avg_energy,
                AVG(spectral_centroid_mean) as avg_spectral_centroid
            FROM acoustic_features
            WHERE voice_entry_id IN (
                SELECT id FROM voice_entries
                WHERE timestamp > datetime('now', '-' || ? || ' days')
            )
        '''
        
        df = pd.read_sql_query(query, self.conn, params=(days,))
        return df
    
    def update_daily_summary(self, date: str, summary: Dict):
        """
        Update daily summary
        
        Args:
            date (str): Date (YYYY-MM-DD)
            summary (dict): Summary data
        """
        insights_json = json.dumps(summary.get('insights', {}))
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO daily_summaries
            (date, avg_burnout_score, max_stress_level, num_entries, overall_mood, insights)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            date,
            summary.get('avg_burnout_score'),
            summary.get('max_stress_level'),
            summary.get('num_entries'),
            summary.get('overall_mood'),
            insights_json
        ))
        
        self.conn.commit()
    
    def get_insights(self, days: int = 30) -> Dict:
        """
        Generate insights from voice journal data
        
        Args:
            days (int): Number of days to analyze
        
        Returns:
            dict: Generated insights
        """
        trend_df = self.get_burnout_trend(days)
        feature_stats = self.get_acoustic_feature_stats(days)
        emotion_dist = self.get_emotion_distribution(days)
        
        insights = {
            'avg_burnout_score': float(trend_df['avg_burnout_score'].mean()) if not trend_df.empty and trend_df['avg_burnout_score'].mean() is not None else 0,
            'highest_burnout_day': str(trend_df.loc[trend_df['avg_burnout_score'].idxmax(), 'date']) if not trend_df.empty else None,
            'emotion_distribution': emotion_dist,
            'avg_jitter': float(feature_stats['avg_jitter'].iloc[0]) if not feature_stats.empty and feature_stats['avg_jitter'].iloc[0] is not None else 0,
            'avg_shimmer': float(feature_stats['avg_shimmer'].iloc[0]) if not feature_stats.empty and feature_stats['avg_shimmer'].iloc[0] is not None else 0,
            'total_entries': int(trend_df['num_entries'].sum()) if not trend_df.empty else 0
        }
        
        return insights
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
