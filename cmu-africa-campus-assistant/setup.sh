
#!/bin/bash

echo "========================================"
echo "CMU-Africa Campus Assistant Setup"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Step 1: Setting up Backend${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup .env
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env and add your API keys:${NC}"
    echo "  - OPENAI_API_KEY"
    echo "  - PINECONE_API_KEY"
fi

cd ..

echo -e "\n${GREEN}Step 2: Setting up Frontend${NC}"
cd frontend

echo "Installing Node.js dependencies..."
npm install

cd ..

echo -e "\n${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your API keys"
echo "2. Load sample knowledge base: cd backend && python load_knowledge_base.py"
echo "3. Start backend: ./start_backend.sh (in one terminal)"
echo "4. Start frontend: ./start_frontend.sh (in another terminal)"
echo ""
echo "Or use the quick start:"
echo "  chmod +x start_backend.sh start_frontend.sh"
echo "  ./start_backend.sh &"
echo "  ./start_frontend.sh"
