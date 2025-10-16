
#!/bin/bash
# View logs for CMU-Africa Campus Assistant containers

echo "======================================"
echo "CMU-Africa Campus Assistant Logs"
echo "======================================"
echo ""

# Check if any service is specified
if [ -z "$1" ]; then
    echo "Showing logs for all services (Press Ctrl+C to exit)..."
    echo ""
    docker compose logs -f
elif [ "$1" == "backend" ]; then
    echo "Showing backend logs (Press Ctrl+C to exit)..."
    echo ""
    docker compose logs -f backend
elif [ "$1" == "frontend" ]; then
    echo "Showing frontend logs (Press Ctrl+C to exit)..."
    echo ""
    docker compose logs -f frontend
else
    echo "Usage: ./docker-logs.sh [service]"
    echo ""
    echo "Services:"
    echo "  backend  - View backend logs only"
    echo "  frontend - View frontend logs only"
    echo "  (no arg) - View all logs"
    echo ""
    echo "Examples:"
    echo "  ./docker-logs.sh"
    echo "  ./docker-logs.sh backend"
    echo "  ./docker-logs.sh frontend"
fi
