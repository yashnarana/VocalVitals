#!/usr/bin/env python3
"""
VocalVitals Setup Script
Installs dependencies and verifies environment
"""

import subprocess
import sys

def run_command(cmd, description=""):
    """Run a shell command and report status"""
    if description:
        print(f"\n🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"✅ Success")
            return True
        else:
            print(f"❌ Failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("🎤 VocalVitals Environment Setup")
    print("=" * 70)
    
    # Install core packages one by one
    packages = [
        ("numpy", "NumPy - Numerical computing"),
        ("librosa", "Librosa - Audio processing"),
        ("scipy", "SciPy - Scientific computing"),
        ("pandas", "Pandas - Data analysis"),
        ("matplotlib", "Matplotlib - Plotting"),
        ("seaborn", "Seaborn - Statistical visualization"),
        ("scikit-learn", "Scikit-learn - Machine learning"),
        ("streamlit", "Streamlit - Web framework"),
    ]
    
    print("\n📦 Installing core packages...")
    print("-" * 70)
    
    for package, description in packages:
        cmd = f"{sys.executable} -m pip install {package} -q"
        run_command(cmd, description)
    
    # Verify installations
    print("\n\n✅ Verifying installations...")
    print("-" * 70)
    
    test_cmd = """
import librosa
import streamlit
import pandas
import numpy
import matplotlib
import scipy
print('✅ All core packages imported successfully!')
"""
    
    cmd = f"{sys.executable} -c \"{test_cmd}\""
    run_command(cmd, "Testing imports")
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print("\n🚀 You can now run:")
    print("   streamlit run app/main.py")
    print("\n")

if __name__ == "__main__":
    main()
