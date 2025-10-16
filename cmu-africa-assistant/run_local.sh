
#!/bin/bash

# CMU-Africa Information Assistant - Local Runner Script

echo "======================================"
echo "CMU-Africa Information Assistant"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the application"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting application..."
echo "Access at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the application
streamlit run src/app.py
