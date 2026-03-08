"""
Dataset Download Utilities
Download and prepare RAVDESS, TESS, and SAVEE datasets
"""

import os
import gdown
import shutil
import zipfile
from pathlib import Path
from tqdm import tqdm


class DatasetDownloader:
    """Download and extract emotion recognition datasets"""
    
    # Google Drive file IDs for datasets
    RAVDESS_ID = "1wWsrSP7sh-I4rVZcLyy2Jxsd-AlIKfFR"  # Example ID - replace with actual
    TESS_ID = "1ngyNgzw-ZF28gwF5-QvmJlTmb65Yp_5X"  # Example ID - replace with actual
    SAVEE_ID = "1EgkXARZ3hGGVPxcMHjNMlkIlNdKn5jzn"  # Example ID - replace with actual
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize downloader
        
        Args:
            data_dir (str): Directory to store datasets
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def download_ravdess(self) -> bool:
        """
        Download RAVDESS dataset (Ryerson Audio-Visual Emotion Database and Speech Set)
        
        Returns:
            bool: Success status
        """
        ravdess_dir = self.data_dir / "RAVDESS"
        
        if ravdess_dir.exists():
            print("✅ RAVDESS dataset already downloaded")
            return True
        
        try:
            print("📥 Downloading RAVDESS dataset...")
            zip_path = self.data_dir / "ravdess.zip"
            
            # Download from Google Drive
            gdown.download(f"https://drive.google.com/uc?id={self.RAVDESS_ID}", 
                          str(zip_path), quiet=False)
            
            # Extract
            print("📦 Extracting RAVDESS...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ravdess_dir)
            
            # Cleanup
            os.remove(zip_path)
            
            print(f"✅ RAVDESS saved to {ravdess_dir}")
            return True
        
        except Exception as e:
            print(f"❌ Error downloading RAVDESS: {e}")
            return False
    
    def download_tess(self) -> bool:
        """
        Download TESS dataset (Toronto Emotional Speech Set)
        
        Returns:
            bool: Success status
        """
        tess_dir = self.data_dir / "TESS"
        
        if tess_dir.exists():
            print("✅ TESS dataset already downloaded")
            return True
        
        try:
            print("📥 Downloading TESS dataset...")
            zip_path = self.data_dir / "tess.zip"
            
            gdown.download(f"https://drive.google.com/uc?id={self.TESS_ID}",
                          str(zip_path), quiet=False)
            
            print("📦 Extracting TESS...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tess_dir)
            
            os.remove(zip_path)
            
            print(f"✅ TESS saved to {tess_dir}")
            return True
        
        except Exception as e:
            print(f"❌ Error downloading TESS: {e}")
            return False
    
    def download_savee(self) -> bool:
        """
        Download SAVEE dataset (Surrey Audio-Visual Expressed Emotion Database)
        
        Returns:
            bool: Success status
        """
        savee_dir = self.data_dir / "SAVEE"
        
        if savee_dir.exists():
            print("✅ SAVEE dataset already downloaded")
            return True
        
        try:
            print("📥 Downloading SAVEE dataset...")
            zip_path = self.data_dir / "savee.zip"
            
            gdown.download(f"https://drive.google.com/uc?id={self.SAVEE_ID}",
                          str(zip_path), quiet=False)
            
            print("📦 Extracting SAVEE...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(savee_dir)
            
            os.remove(zip_path)
            
            print(f"✅ SAVEE saved to {savee_dir}")
            return True
        
        except Exception as e:
            print(f"❌ Error downloading SAVEE: {e}")
            return False
    
    def download_all(self) -> dict:
        """
        Download all datasets
        
        Returns:
            dict: Status of each dataset
        """
        print("\n" + "="*50)
        print("🎵 Downloading Emotion Recognition Datasets")
        print("="*50 + "\n")
        
        results = {
            'ravdess': self.download_ravdess(),
            'tess': self.download_tess(),
            'savee': self.download_savee()
        }
        
        print("\n" + "="*50)
        print("📊 Download Summary")
        print("="*50)
        
        for dataset, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"{dataset.upper()}: {status}")
        
        return results


if __name__ == "__main__":
    downloader = DatasetDownloader()
    results = downloader.download_all()
    
    print("\n💡 Next steps:")
    print("1. Run: python train_model.py")
    print("2. Launch: streamlit run app/main.py")
