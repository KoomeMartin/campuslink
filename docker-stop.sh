
#!/bin/bash
# Stop all Docker containers for CMU-Africa Campus Assistant

echo "======================================"
echo "Stopping CMU-Africa Campus Assistant"
echo "======================================"
echo ""

# Stop containers
docker compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Containers stopped successfully!"
    echo ""
    echo "To start again: ./docker-start.sh"
else
    echo ""
    echo "❌ Failed to stop containers! Please check the errors above."
    exit 1
fi
