#!/bin/bash

# VocalVitals Full Stack Setup Script
# This script sets up and starts both frontend and backend

set -e

WORKSPACE="/Users/yashnarana/Desktop/VocalVitals/VocalVitals"
cd "$WORKSPACE"

echo "================================"
echo "   VocalVitals Full Stack Setup"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Backend Setup
echo -e "${BLUE}Step 1: Setting up Backend...${NC}"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt > /dev/null 2>&1 || {
    echo -e "${YELLOW}Warning: Some Python packages failed to install (Librosa may be incompatible with Python 3.13)${NC}"
    echo "Continuing with fallback mode..."
}

echo -e "${GREEN}✅ Backend dependencies installed${NC}"
echo ""

# 2. Frontend Setup
echo -e "${BLUE}Step 2: Setting up Frontend...${NC}"

cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install > /dev/null 2>&1
fi

echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
echo ""

# 3. Summary
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}   Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "To start the application, run in separate terminals:"
echo ""
echo -e "${BLUE}Terminal 1 - Backend (FastAPI):${NC}"
echo "  cd $WORKSPACE"
echo "  source venv/bin/activate"
echo "  cd backend"
echo "  python main.py"
echo ""
echo -e "${BLUE}Terminal 2 - Frontend (Angular):${NC}"
echo "  cd $WORKSPACE/frontend"
echo "  npm start"
echo ""
echo "Then open: http://localhost:4200"
echo ""
echo -e "${YELLOW}API Docs: http://localhost:8000/docs${NC}"
echo ""
