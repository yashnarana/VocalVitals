#!/bin/bash

# Start VocalVitals Full Stack (Streamlit Frontend & FastAPI Backend)
# Run this script in the project root

set -e

WORKSPACE="/Users/yashnarana/Desktop/VocalVitals/VocalVitals"

echo "Starting VocalVitals Full Stack Application..."
echo ""
echo "Make sure you have Python installed."
echo "Run 'pip install -r requirements.txt' first if you haven't already."
echo ""

# Kill any existing processes on ports 8000 and 8501
echo "Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8501 | xargs kill -9 2>/dev/null || true

echo "Starting Backend (FastAPI on port 8000)..."
cd "$WORKSPACE"
source .venv/bin/activate
cd backend

# Background process for backend
python main.py &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
sleep 3

echo ""
echo "Starting Frontend (Streamlit on port 8501)..."
cd "$WORKSPACE/frontend"
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
sleep 3

echo ""
echo "========================================="
echo "✅ VocalVitals is running!"
echo "========================================="
echo ""
echo "Frontend: http://localhost:8501"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
