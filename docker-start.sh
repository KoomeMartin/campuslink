
#!/bin/bash
# Start all Docker containers for CMU-Africa Campus Assistant

echo "======================================"
echo "Starting CMU-Africa Campus Assistant"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your API keys."
    exit 1
fi

# Source .env file to check for required variables
source .env

# Check required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ -z "$PINECONE_API_KEY" ] || [ -z "$PINECONE_ENVIRONMENT" ]; then
    echo "❌ Error: Missing required environment variables!"
    echo "Please ensure your .env file contains:"
    echo "  - OPENAI_API_KEY"
    echo "  - PINECONE_API_KEY"
    echo "  - PINECONE_ENVIRONMENT"
    exit 1
fi

echo "Starting containers..."
echo ""

# Start containers
docker compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Containers started successfully!"
    echo ""
    echo "Services:"
    echo "  Frontend: http://localhost"
    echo "  Backend:  http://localhost:8001"
    echo "  API Docs: http://localhost:8001/docs"
    echo ""
    echo "To view logs: ./docker-logs.sh"
    echo "To stop:      ./docker-stop.sh"
    echo ""
    echo "Checking container status..."
    docker compose ps
else
    echo ""
    echo "❌ Failed to start containers! Please check the errors above."
    exit 1
fi
