#!/bin/bash
# Start CMU-Africa Campus Assistant (Native Mode)

echo "=========================================="
echo "Starting CMU-Africa Campus Assistant"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys."
    exit 1
fi

# Start backend
echo "Starting backend server on port 8001..."
cd backend
source venv/bin/activate
nohup gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend server on port 3000..."
cd frontend/build
nohup python3 -m http.server 3000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ../..

# Wait and check health
sleep 2
echo ""
echo "Checking application health..."
HEALTH=$(curl -s http://localhost:8001/health)
if [[ $HEALTH == *"healthy"* ]]; then
    echo "✅ Application started successfully!"
    echo ""
    echo "Access the application:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8001"
    echo "  API Docs: http://localhost:8001/docs"
    echo ""
    echo "View logs:"
    echo "  Backend: tail -f /tmp/backend.log"
    echo "  Frontend: tail -f /tmp/frontend.log"
    echo ""
    echo "To stop the application, run: ./stop-app.sh"
else
    echo "❌ Backend health check failed"
    echo "Check logs: tail -f /tmp/backend.log"
    exit 1
fi
