
#!/bin/bash

echo "========================================"
echo "Starting CMU-Africa Assistant Backend"
echo "========================================"

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env file with your API keys:"
    echo "  cp .env.example .env"
    echo "  Then edit .env and add your keys"
    exit 1
fi

# Start server
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop"
python main.py
