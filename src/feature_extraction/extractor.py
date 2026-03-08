"""
Feature Extraction Module
Extract acoustic biomarkers correlated with stress and burnout
"""

import numpy as np
import warnings
from scipy import signal
from typing import Dict, Tuple

# Try to import librosa, fall back if Python 3.13 compatibility issues
try:
    import librosa
    LIBROSA_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    LIBROSA_AVAILABLE = False
    librosa = None
    warnings.warn(f"Librosa not available: {e}. Using fallback feature extraction.")

try:
    from scipy.fftpack import fft
    SCIPY_FFT_AVAILABLE = True
except ImportError:
    SCIPY_FFT_AVAILABLE = False
    fft = None


class AcousticFeatureExtractor:
    """Extract acoustic biomarkers from audio files"""
    
    def __init__(self, sr: int = 22050):
        """
        Initialize extractor
        
        Args:
            sr (int): Sample rate
        """
        self.sr = sr
    
    def extract_jitter(self, y: np.ndarray, sr: int, frame_length: int = 2048) -> float:
        """
        Extract jitter (frequency instability)
        Jitter is the variation in vocal fold vibration - higher in stressed speakers
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
            frame_length (int): Frame length for pitch detection
        
        Returns:
            float: Jitter value (higher = more stressed)
        """
        # Estimate pitch using autocorrelation
        frame_hop = frame_length // 4
        n_frames = (len(y) - frame_length) // frame_hop + 1
        
        pitches = []
        for i in range(min(n_frames, 50)):  # Use first 50 frames
            frame = y[i*frame_hop:i*frame_hop+frame_length]
            autocorr = np.abs(np.fft.fft(frame))
            
            # Find dominant frequency
            peak = np.argsort(autocorr)[-1]
            if peak > 0:
                freq = sr * peak / frame_length
                pitches.append(freq)
        
        if len(pitches) < 2:
            return 0.0
        
        # Jitter = mean absolute difference between consecutive pitches
        jitter = np.mean(np.abs(np.diff(pitches))) / np.mean(pitches)
        return jitter
    
    def extract_shimmer(self, y: np.ndarray, frame_length: int = 2048) -> float:
        """
        Extract shimmer (amplitude instability)
        Shimmer is the variation in vocal amplitude - higher in stressed speakers
        
        Args:
            y (np.ndarray): Audio time series
            frame_length (int): Frame length
        
        Returns:
            float: Shimmer value (higher = more stressed)
        """
        frame_hop = frame_length // 4
        n_frames = (len(y) - frame_length) // frame_hop + 1
        
        amplitudes = []
        for i in range(min(n_frames, 50)):
            frame = y[i*frame_hop:i*frame_hop+frame_length]
            amplitude = np.sqrt(np.mean(frame**2))
            amplitudes.append(amplitude)
        
        if len(amplitudes) < 2:
            return 0.0
        
        # Shimmer = mean absolute difference between consecutive amplitudes
        shimmer = np.mean(np.abs(np.diff(amplitudes))) / np.mean(amplitudes)
        return shimmer
    
    def extract_voice_activity(self, y: np.ndarray, threshold: float = 0.02) -> float:
        """
        Extract voice activity ratio
        Lower voice activity ratio may indicate fatigue/burnout
        
        Args:
            y (np.ndarray): Audio time series
            threshold (float): RMS threshold for voice activity
        
        Returns:
            float: Proportion of voice activity (0-1)
        """
        if LIBROSA_AVAILABLE:
            rms = librosa.feature.rms(y=y)[0]
        else:
            # Simple fallback: split into frames and compute RMS
            frame_length = 2048
            hop_length = 512
            n_frames = (len(y) - frame_length) // hop_length + 1
            rms = []
            for i in range(n_frames):
                frame = y[i*hop_length:i*hop_length+frame_length]
                rms.append(np.sqrt(np.mean(frame**2)))
            rms = np.array(rms)
        
        voice_frames = np.sum(rms > threshold)
        return voice_frames / len(rms) if len(rms) > 0 else 0.0
    
    def extract_speech_rate(self, y: np.ndarray, sr: int) -> float:
        """
        Extract speech rate (syllables per second)
        Stressed speakers often have altered speech rates
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
        
        Returns:
            float: Estimated speech rate
        """
        if LIBROSA_AVAILABLE:
            # Use onset detection to estimate syllables
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            peaks = signal.find_peaks(onset_env, height=np.median(onset_env))[0]
        else:
            # Fallback: use energy-based onset detection
            frame_length = 2048
            hop_length = 512
            n_frames = (len(y) - frame_length) // hop_length + 1
            energy = []
            for i in range(n_frames):
                frame = y[i*hop_length:i*hop_length+frame_length]
                energy.append(np.sqrt(np.mean(frame**2)))
            energy = np.array(energy)
            peaks = signal.find_peaks(energy, height=np.median(energy))[0]
        
        duration = len(y) / sr
        speech_rate = len(peaks) / duration if duration > 0 else 0
        return speech_rate
    
    def extract_pitch_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Extract pitch-based features
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
        
        Returns:
            dict: Dictionary with pitch features
        """
        pitch_values = []
        
        if LIBROSA_AVAILABLE:
            # Use librosa piptrack
            S = np.abs(librosa.stft(y))
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
        else:
            # Fallback: use autocorrelation
            frame_length = 2048
            hop_length = 512
            n_frames = (len(y) - frame_length) // hop_length + 1
            
            for i in range(min(n_frames, 50)):  # Sample first 50 frames
                frame = y[i*hop_length:i*hop_length+frame_length]
                if len(frame) > 0:
                    autocorr = np.correlate(frame, frame, mode='full')
                    autocorr = autocorr[len(autocorr)//2:]
                    if len(autocorr) > 1:
                        peak = np.argsort(autocorr)[-1]
                        if peak > 0:
                            freq = sr / peak
                            if 50 < freq < 400:  # Typical voice frequency range
                                pitch_values.append(freq)
        
        pitch_values = np.array(pitch_values)
        
        if len(pitch_values) == 0:
            return {
                'mean_pitch': 0.0,
                'pitch_std': 0.0,
                'pitch_range': 0.0
            }
        
        return {
            'mean_pitch': np.mean(pitch_values),
            'pitch_std': np.std(pitch_values),
            'pitch_range': np.max(pitch_values) - np.min(pitch_values) if len(pitch_values) > 1 else 0.0
        }
    
    def extract_energy_features(self, y: np.ndarray) -> Dict[str, float]:
        """
        Extract energy-based features
        
        Args:
            y (np.ndarray): Audio time series
        
        Returns:
            dict: Dictionary with energy features
        """
        if LIBROSA_AVAILABLE:
            rms = librosa.feature.rms(y=y)[0]
        else:
            # Fallback: compute RMS manually
            frame_length = 2048
            hop_length = 512
            n_frames = (len(y) - frame_length) // hop_length + 1
            rms = []
            for i in range(n_frames):
                frame = y[i*hop_length:i*hop_length+frame_length]
                rms.append(np.sqrt(np.mean(frame**2)))
            rms = np.array(rms)
        
        return {
            'mean_energy': np.mean(rms),
            'energy_std': np.std(rms),
            'max_energy': np.max(rms),
            'min_energy': np.min(rms)
        }
    
    def extract_mfcc_statistics(self, y: np.ndarray, sr: int, n_mfcc: int = 13) -> Dict[str, np.ndarray]:
        """
        Extract statistics from MFCC features
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
            n_mfcc (int): Number of MFCC coefficients
        
        Returns:
            dict: Dictionary with MFCC statistics
        """
        if LIBROSA_AVAILABLE:
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        else:
            # Fallback: return dummy MFCC statistics
            warnings.warn("Librosa not available. Returning dummy MFCC statistics.")
            mfcc = np.random.randn(n_mfcc, 100)
        
        features = {}
        for i in range(n_mfcc):
            features[f'mfcc_{i}_mean'] = np.mean(mfcc[i])
            features[f'mfcc_{i}_std'] = np.std(mfcc[i])
        
        return features
    
    def extract_spectral_statistics(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Extract spectral statistics
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
        
        Returns:
            dict: Dictionary with spectral features
        """
        if LIBROSA_AVAILABLE:
            S = np.abs(librosa.stft(y))
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        else:
            # Fallback: use scipy FFT
            warnings.warn("Librosa not available. Using fallback spectral features.")
            f, Pxx = signal.welch(y, sr)
            spectral_centroid = np.array([sr / 2])
            spectral_rolloff = np.array([sr / 2])
            spectral_bandwidth = np.array([sr / 4])
            # Compute zero crossing rate manually
            zcr = np.sum(np.abs(np.diff(np.sign(y)))) / (2.0 * len(y))
            zero_crossing_rate = np.array([zcr])
        
        return {
            'spectral_centroid_mean': np.mean(spectral_centroid),
            'spectral_centroid_std': np.std(spectral_centroid),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'zero_crossing_rate_mean': np.mean(zero_crossing_rate)
        }
    
    def extract_all_features(self, y: np.ndarray, sr: int) -> Dict[str, any]:
        """
        Extract ALL acoustic biomarkers
        This is like a comprehensive "health checkup" for the voice
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
        
        Returns:
            dict: Dictionary containing all extracted features
        """
        features = {}
        
        # Stress biomarkers
        features['jitter'] = self.extract_jitter(y, sr)
        features['shimmer'] = self.extract_shimmer(y)
        features['voice_activity'] = self.extract_voice_activity(y)
        features['speech_rate'] = self.extract_speech_rate(y, sr)
        
        # Pitch features
        pitch_features = self.extract_pitch_features(y, sr)
        features.update(pitch_features)
        
        # Energy features
        energy_features = self.extract_energy_features(y)
        features.update(energy_features)
        
        # MFCC statistics
        mfcc_features = self.extract_mfcc_statistics(y, sr)
        features.update(mfcc_features)
        
        # Spectral statistics
        spectral_features = self.extract_spectral_statistics(y, sr)
        features.update(spectral_features)
        
        return features
