#!/bin/bash

# VocalVitals Setup & Quick Start Guide
# This script helps you set up the complete VocalVitals environment

echo "======================================================================"
echo "🎤 VocalVitals - Speech Emotion & Burnout Tracker"
echo "======================================================================"
echo ""

# Check Python version
echo "🔍 Checking Python installation..."
python3 --version

# Create virtual environment
echo ""
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
echo "   This will take 2-5 minutes..."
pip install --upgrade pip
pip install -r requirements.txt

# Create required directories
echo ""
echo "📁 Creating project directories..."
mkdir -p data/raw data/processed
mkdir -p models logs database

echo ""
echo "======================================================================"
echo "✅ SETUP COMPLETE!"
echo "======================================================================"
echo ""

echo "📖 QUICK START GUIDE:"
echo ""
echo "1️⃣  LAUNCH STREAMLIT DASHBOARD:"
echo "   streamlit run app/main.py"
echo "   → Opens at: http://localhost:8501"
echo ""

echo "2️⃣  RUN JUPYTER NOTEBOOK (Optional):"
echo "   jupyter notebook notebooks/VocalVitals_Exploration.ipynb"
echo ""

echo "3️⃣  DOWNLOAD EMOTION DATASETS (Optional, ~3GB):"
echo "   python src/utils/download_datasets.py"
echo ""

echo "4️⃣  TRAIN YOUR OWN MODELS:"
echo "   python train_model.py"
echo ""

echo "======================================================================"
echo "📋 NEXT STEPS:"
echo "======================================================================"
echo ""
echo "✨ Now you can:"
echo ""
echo "   📔 Record & Analyze Your Voice"
echo "   • Upload audio files or record live"
echo "   • Get instant emotion classification"
echo "   • See burnout score (0-100)"
echo "   • View stress indicators"
echo ""

echo "   📊 Track Burnout Over Time"
echo "   • Voice Journal with timestamps"
echo "   • Trend analysis dashboard"
echo "   • Weekly/Monthly patterns"
echo "   • AI-powered insights"
echo ""

echo "   🧠 Train & Improve Models"
echo "   • Use RAVDESS, TESS, SAVEE datasets"
echo "   • Custom model training"
echo "   • Fine-tune for your voice"
echo ""

echo "======================================================================"
echo "🎓 LEARNING RESOURCES:"
echo "======================================================================"
echo ""
echo "📚 Within This Project:"
echo "   • README.md - Full documentation (70KB)"
echo "   • notebooks/VocalVitals_Exploration.ipynb - Interactive tutorial"
echo "   • src/ - Modular, well-documented code"
echo ""

echo "🌐 External Resources:"
echo "   • Librosa Audio Processing: https://librosa.org/"
echo "   • TensorFlow Deep Learning: https://tensorflow.org/"
echo "   • Streamlit Docs: https://docs.streamlit.io/"
echo "   • Speech Emotion Research: https://scholar.google.com/"
echo ""

echo "======================================================================"
echo "❓ QUICK ANSWERS:"
echo "======================================================================"
echo ""
echo "Q: How do I record my voice?"
echo "A: Use Streamlit app → 'Analyze Voice' → Upload or record"
echo ""

echo "Q: What does burnout score mean?"
echo "A: 0-25: Healthy, 25-50: Mild, 50-75: Moderate, 75-100: Severe"
echo ""

echo "Q: Can I use real datasets?"
echo "A: Yes! Run: python src/utils/download_datasets.py"
echo ""

echo "Q: How is my data stored?"
echo "A: Locally in SQLite (database/voice_journal.db)"
echo ""

echo "Q: Is this a medical device?"
echo "A: No! It's educational/research. Consult healthcare professionals."
echo ""

echo "======================================================================"
echo "🚨 IMPORTANT DISCLAIMER:"
echo "======================================================================"
echo ""
echo "VocalVitals is a research tool, NOT a medical diagnostic device."
echo "For burnout, anxiety, or depression - consult qualified professionals:"
echo ""
echo "   🆘 SAMHSA National Helpline: 1-800-662-4357"
echo "   💬 Crisis Text Line: Text HOME to 741741"
echo ""

echo "======================================================================"
echo ""
echo "Ready to analyze your voice! 🎤"
echo ""
echo "Run: streamlit run app/main.py"
echo ""
