
#!/bin/bash
# Build all Docker images for CMU-Africa Campus Assistant

echo "======================================"
echo "Building CMU-Africa Campus Assistant"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please copy .env.example to .env and fill in your API keys."
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Building Docker images..."
echo ""

# Build images
docker compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker images built successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Make sure your .env file has valid API keys"
    echo "2. Run ./docker-start.sh to start the application"
else
    echo ""
    echo "❌ Build failed! Please check the errors above."
    exit 1
fi
