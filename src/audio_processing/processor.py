"""
Audio Processing Module
Handles audio file loading, preprocessing, and spectrogram generation
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple, Optional
import warnings

# Try to import librosa, fall back if Python 3.13 compatibility issues
try:
    import librosa
    import librosa.display
    LIBROSA_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    LIBROSA_AVAILABLE = False
    librosa = None
    warnings.warn(f"Librosa not available: {e}. Using fallback audio processing.")

try:
    from scipy import signal
    from scipy.io import wavfile
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    signal = None
    wavfile = None


class AudioProcessor:
    """Load, process, and analyze audio files"""
    
    def __init__(self, sr: int = 22050, n_mels: int = 128, n_fft: int = 2048):
        """
        Initialize audio processor
        
        Args:
            sr (int): Sample rate (default 22050 Hz)
            n_mels (int): Number of mel frequency bins (default 128)
            n_fft (int): FFT window size (default 2048)
        """
        self.sr = sr
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = n_fft // 4
    
    def load_audio(self, file_path: str, duration: Optional[float] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file
        
        Args:
            file_path (str): Path to audio file
            duration (float, optional): Duration in seconds to load
        
        Returns:
            Tuple[np.ndarray, int]: Audio time series and sample rate
        """
        if LIBROSA_AVAILABLE:
            try:
                y, sr = librosa.load(file_path, sr=self.sr, duration=duration)
                return y, sr
            except Exception as e:
                raise ValueError(f"Error loading audio file {file_path}: {str(e)}")
        elif SCIPY_AVAILABLE:
            try:
                sr, y = wavfile.read(file_path)
                # Resample to target sample rate
                if sr != self.sr:
                    num_samples = int(len(y) * self.sr / sr)
                    y = signal.resample(y, num_samples)
                    sr = self.sr
                # Convert to mono if stereo
                if len(y.shape) > 1:
                    y = np.mean(y, axis=1)
                # Normalize to [-1, 1]
                y = y.astype(np.float32) / np.max(np.abs(y))
                return y, sr
            except Exception as e:
                raise ValueError(f"Error loading audio file {file_path} using scipy: {str(e)}")
        else:
            raise ImportError("Neither librosa nor scipy available for audio loading")
    
    def generate_mel_spectrogram(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Generate Mel-spectrogram from audio time series
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
        
        Returns:
            np.ndarray: Mel-spectrogram (log-scaled)
        """
        if LIBROSA_AVAILABLE:
            mel_spec = librosa.feature.melspectrogram(
                y=y,
                sr=sr,
                n_mels=self.n_mels,
                n_fft=self.n_fft,
                hop_length=self.hop_length
            )
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            return mel_spec_db
        else:
            # Fallback: use scipy.signal for STFT
            if SCIPY_AVAILABLE:
                f, t, Sxx = signal.spectrogram(y, sr, nperseg=self.n_fft)
                # Simple log scale
                Sxx_db = 10 * np.log10(np.abs(Sxx) + 1e-10)
                return Sxx_db
            else:
                # Return dummy spectrogram
                warnings.warn("Cannot compute mel-spectrogram without librosa or scipy")
                return np.ones((self.n_mels, 100))
    
    def generate_mfcc(self, y: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
        """
        Generate MFCC (Mel-Frequency Cepstral Coefficients)
        
        Args:
            y (np.ndarray): Audio time series
            sr (int): Sample rate
            n_mfcc (int): Number of MFCC features
        
        Returns:
            np.ndarray: MFCC features
        """
        if LIBROSA_AVAILABLE:
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
            return mfcc
        else:
            warnings.warn("Librosa not available. Returning dummy MFCC features.")
            return np.random.randn(n_mfcc, 100)
    
    def extract_zero_crossing_rate(self, y: np.ndarray) -> np.ndarray:
        """Extract zero-crossing rate"""
        if LIBROSA_AVAILABLE:
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            return zcr
        else:
            # Compute zero crossing rate manually
            zcr = np.sum(np.abs(np.diff(np.sign(y)))) / (2.0 * len(y))
            return np.array([zcr])
    
    def extract_spectral_features(self, y: np.ndarray, sr: int) -> dict:
        """
        Extract various spectral features
        
        Returns:
            dict: Dictionary containing spectral features
        """
        features = {}
        
        if LIBROSA_AVAILABLE:
            # Spectral centroid
            features['spectral_centroid'] = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            
            # Spectral rolloff
            features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Zero crossing rate
            features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y)[0]
            
            # RMS Energy
            features['rms_energy'] = librosa.feature.rms(y=y)[0]
        else:
            # Fallback: simple features
            warnings.warn("Librosa not available. Using simplified spectral features.")
            features['spectral_centroid'] = np.array([sr / 2])  # Simple default
            features['spectral_rolloff'] = np.array([sr / 2])
            features['zero_crossing_rate'] = np.array([0.1])  # Simple default
            features['rms_energy'] = np.array([np.sqrt(np.mean(y ** 2))])
        
        return features
    
    def normalize_spectrogram(self, mel_spec: np.ndarray, 
                             mean: Optional[np.ndarray] = None,
                             std: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Normalize spectrogram using mean and std
        
        Args:
            mel_spec (np.ndarray): Mel-spectrogram
            mean (np.ndarray, optional): Pre-computed mean
            std (np.ndarray, optional): Pre-computed std
        
        Returns:
            Tuple: Normalized spectrogram, mean, std
        """
        if mean is None:
            mean = np.mean(mel_spec, axis=1, keepdims=True)
        if std is None:
            std = np.std(mel_spec, axis=1, keepdims=True)
        
        normalized = (mel_spec - mean) / (std + 1e-9)
        return normalized, mean, std
    
    def pad_or_truncate(self, spectrogram: np.ndarray, 
                       target_length: int) -> np.ndarray:
        """
        Pad or truncate spectrogram to target length
        
        Args:
            spectrogram (np.ndarray): Input spectrogram
            target_length (int): Target time dimension length
        
        Returns:
            np.ndarray: Padded or truncated spectrogram
        """
        _, current_length = spectrogram.shape
        
        if current_length < target_length:
            # Pad with zeros
            pad_width = ((0, 0), (0, target_length - current_length))
            return np.pad(spectrogram, pad_width, mode='constant', constant_values=0)
        else:
            # Truncate
            return spectrogram[:, :target_length]
    
    def visualize_spectrogram(self, mel_spec: np.ndarray, sr: int = 22050,
                             title: str = "Mel-Spectrogram") -> None:
        """
        Visualize mel-spectrogram
        
        Args:
            mel_spec (np.ndarray): Mel-spectrogram
            sr (int): Sample rate
            title (str): Plot title
        """
        fig, ax = plt.subplots(figsize=(12, 4))
        if LIBROSA_AVAILABLE:
            img = librosa.display.specshow(mel_spec, sr=sr, hop_length=self.hop_length,
                                           x_axis='time', y_axis='mel', ax=ax)
        else:
            # Fallback: use imshow
            img = ax.imshow(mel_spec, aspect='auto', origin='lower')
        ax.set_title(title)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')
        plt.tight_layout()
        plt.show()
    
    def process_audio_file(self, file_path: str, 
                          target_length: int = 128,
                          normalize: bool = True) -> dict:
        """
        Complete audio processing pipeline
        
        Args:
            file_path (str): Path to audio file
            target_length (int): Target spectrogram length
            normalize (bool): Whether to normalize the spectrogram
        
        Returns:
            dict: Dictionary containing processed audio features
        """
        # Load audio
        y, sr = self.load_audio(file_path)
        
        # Generate mel-spectrogram
        mel_spec = self.generate_mel_spectrogram(y, sr)
        
        # Extract additional features
        spectral_features = self.extract_spectral_features(y, sr)
        mfcc = self.generate_mfcc(y, sr)
        
        # Normalize if requested
        if normalize:
            mel_spec, mean, std = self.normalize_spectrogram(mel_spec)
        else:
            mean, std = None, None
        
        # Pad or truncate
        mel_spec = self.pad_or_truncate(mel_spec, target_length)
        
        return {
            'mel_spectrogram': mel_spec,
            'mfcc': mfcc,
            'spectral_features': spectral_features,
            'audio_time_series': y,
            'sample_rate': sr,
            'normalization_params': {'mean': mean, 'std': std}
        }
