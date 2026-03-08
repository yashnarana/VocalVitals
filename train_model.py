"""
Model Training Script
Train emotion classification and burnout detection models
"""

import setuptools  # Must be before tensorflow for Python 3.12 compatibility

import os
import numpy as np
import tensorflow as tf
import keras
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from pathlib import Path
import sys

# Add src directory
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, os.path.join(Path(__file__).parent, 'src'))

from audio_processing.processor import AudioProcessor
from feature_extraction.extractor import AcousticFeatureExtractor
from models.emotion_models import create_emotion_cnn, create_burnout_classifier


class ModelTrainer:
    """Train deep learning models for emotion and burnout detection"""
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize trainer
        
        Args:
            model_dir (str): Directory to save trained models
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.audio_processor = AudioProcessor()
        self.feature_extractor = AcousticFeatureExtractor()
    
    def prepare_mel_spectrograms(self, audio_paths: list, emotion_labels: list,
                                target_shape: tuple = (128, 128)) -> tuple:
        """
        Prepare mel-spectrograms for CNN training
        
        Args:
            audio_paths (list): List of audio file paths
            emotion_labels (list): Corresponding emotion labels
            target_shape (tuple): Target spectrogram shape
        
        Returns:
            tuple: (spectrograms, labels)
        """
        print(f"📊 Preparing {len(audio_paths)} mel-spectrograms...")
        
        spectrograms = []
        processed_labels = []
        
        emotion_to_idx = {
            'neutral': 0, 'calm': 1, 'happy': 2, 'frustrated': 3,
            'sad': 4, 'angry': 5, 'fearful': 6
        }
        
        for i, (audio_path, label) in enumerate(zip(audio_paths, emotion_labels)):
            if i % 100 == 0:
                print(f"  Processing {i}/{len(audio_paths)}...")
            
            try:
                # Load and process audio
                y, sr = self.audio_processor.load_audio(audio_path)
                mel_spec = self.audio_processor.generate_mel_spectrogram(y, sr)
                
                # Normalize and resize
                mel_spec, _, _ = self.audio_processor.normalize_spectrogram(mel_spec)
                mel_spec = self.audio_processor.pad_or_truncate(mel_spec, target_shape[1])
                
                # Ensure correct shape
                if mel_spec.shape[0] > target_shape[0]:
                    mel_spec = mel_spec[:target_shape[0], :]
                elif mel_spec.shape[0] < target_shape[0]:
                    pad_width = ((0, target_shape[0] - mel_spec.shape[0]), (0, 0))
                    mel_spec = np.pad(mel_spec, pad_width, mode='constant')
                
                spectrograms.append(mel_spec)
                processed_labels.append(emotion_to_idx.get(label.lower(), 0))
            
            except Exception as e:
                print(f"  ⚠️ Error processing {audio_path}: {e}")
                continue
        
        spectrograms = np.array(spectrograms)
        spectrograms = spectrograms[..., np.newaxis]  # Add channel dimension
        labels = tf.keras.utils.to_categorical(processed_labels, num_classes=7)
        
        print(f"✅ Prepared {len(spectrograms)} spectrograms")
        print(f"  Shape: {spectrograms.shape}")
        
        return spectrograms, labels
    
    def prepare_acoustic_features(self, audio_paths: list, burnout_labels: list) -> tuple:
        """
        Prepare acoustic features for burnout classifier
        
        Args:
            audio_paths (list): List of audio file paths
            burnout_labels (list): Burnout severity labels (0-3)
        
        Returns:
            tuple: (features, labels)
        """
        print(f"🎤 Preparing acoustic features from {len(audio_paths)} files...")
        
        all_features = []
        processed_labels = []
        
        for i, (audio_path, label) in enumerate(zip(audio_paths, burnout_labels)):
            if i % 100 == 0:
                print(f"  Processing {i}/{len(audio_paths)}...")
            
            try:
                # Load and extract features
                y, sr = self.audio_processor.load_audio(audio_path)
                features = self.feature_extractor.extract_all_features(y, sr)
                
                # Convert to feature vector (in order)
                feature_vector = [
                    features.get('jitter', 0),
                    features.get('shimmer', 0),
                    features.get('voice_activity', 0),
                    features.get('speech_rate', 0),
                    features.get('mean_pitch', 0),
                    features.get('pitch_std', 0),
                    features.get('pitch_range', 0),
                    features.get('mean_energy', 0),
                    features.get('energy_std', 0),
                    features.get('max_energy', 0),
                    features.get('min_energy', 0),
                    features.get('spectral_centroid_mean', 0),
                    features.get('spectral_rolloff_mean', 0),
                    features.get('spectral_bandwidth_mean', 0),
                    features.get('zero_crossing_rate_mean', 0),
                ]
                
                # Add MFCC statistics
                for j in range(13):
                    feature_vector.append(features.get(f'mfcc_{j}_mean', 0))
                    feature_vector.append(features.get(f'mfcc_{j}_std', 0))
                
                all_features.append(feature_vector)
                processed_labels.append(label)
            
            except Exception as e:
                print(f"  ⚠️ Error processing {audio_path}: {e}")
                continue
        
        features_array = np.array(all_features)
        labels = tf.keras.utils.to_categorical(processed_labels, num_classes=4)
        
        print(f"✅ Prepared {len(features_array)} feature vectors")
        print(f"  Shape: {features_array.shape}")
        
        return features_array, labels
    
    def train_emotion_cnn(self, x_train: np.ndarray, y_train: np.ndarray,
                         x_val: np.ndarray, y_val: np.ndarray,
                         epochs: int = 50, batch_size: int = 32) -> None:
        """
        Train emotion classification CNN
        
        Args:
            x_train: Training spectrograms
            y_train: Training labels
            x_val: Validation spectrograms
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
        """
        print("\n" + "="*50)
        print("🧠 Training Emotion CNN")
        print("="*50 + "\n")
        
        model = create_emotion_cnn(input_shape=x_train.shape[1:], num_classes=7)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ModelCheckpoint(
                self.model_dir / 'emotion_cnn_best.h5',
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        # Train
        history = model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save(self.model_dir / 'emotion_cnn_final.h5')
        print(f"✅ Emotion CNN saved to {self.model_dir / 'emotion_cnn_final.h5'}")
        
        return history
    
    def train_burnout_classifier(self, x_train: np.ndarray, y_train: np.ndarray,
                               x_val: np.ndarray, y_val: np.ndarray,
                               epochs: int = 50, batch_size: int = 32) -> None:
        """
        Train burnout detection classifier
        
        Args:
            x_train: Training features
            y_train: Training labels
            x_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
        """
        print("\n" + "="*50)
        print("🔥 Training Burnout Classifier")
        print("="*50 + "\n")
        
        model = create_burnout_classifier(input_features=x_train.shape[1], num_classes=4)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ModelCheckpoint(
                self.model_dir / 'burnout_classifier_best.h5',
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        # Train
        history = model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        model.save(self.model_dir / 'burnout_classifier_final.h5')
        print(f"✅ Burnout classifier saved to {self.model_dir / 'burnout_classifier_final.h5'}")
        
        return history


def main():
    """Main training function"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     VocalVitals Model Training Pipeline                   ║
    ║     Speech Emotion & Burnout Detection                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    trainer = ModelTrainer()
    
    print("""
    ⚠️  BEFORE TRAINING:
    1. Download datasets:
       python src/utils/download_datasets.py
    
    2. Organize your data:
       data/raw/RAVDESS/
       data/raw/TESS/
       data/raw/SAVEE/
    
    ℹ️  NOTE:
    This script is a template. You need to:
    1. Collect or download emotion datasets (RAVDESS, TESS, SAVEE)
    2. Extract audio files and create label mappings
    3. Call trainer methods with your data files
    
    📝 Example usage:
    
    # Prepare data
    audio_files = ['data/raw/RAVDESS/Actor_01/03-01-01-01-01-01-01.wav', ...]
    emotion_labels = ['neutral', 'calm', 'happy', ...]
    
    # Train emotion CNN
    x_train, y_train = trainer.prepare_mel_spectrograms(audio_files, emotion_labels)
    trainer.train_emotion_cnn(x_train, y_train, x_val, y_val)
    """)
    
    print("\n✅ Trainer initialized. Ready to train models!")


if __name__ == "__main__":
    main()
