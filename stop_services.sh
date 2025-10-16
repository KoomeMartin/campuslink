#!/bin/bash

echo "========================================"
echo "Stopping CMU-Africa Assistant Services"
echo "========================================"

# Stop backend
echo "Stopping backend (port 8001)..."
pkill -f "python main.py" 2>/dev/null || pkill -f "uvicorn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend stopped"
else
    echo "⚠️  Backend was not running"
fi

# Stop frontend
echo "Stopping frontend (port 3000)..."
pkill -f "react-scripts start" 2>/dev/null || pkill -f "npm start" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Frontend stopped"
else
    echo "⚠️  Frontend was not running"
fi

echo ""
echo "Checking remaining processes..."
sleep 2

BACKEND_RUNNING=$(netstat -tulnp 2>/dev/null | grep 8001)
FRONTEND_RUNNING=$(netstat -tulnp 2>/dev/null | grep 3000)

if [ -z "$BACKEND_RUNNING" ] && [ -z "$FRONTEND_RUNNING" ]; then
    echo "✅ All services stopped successfully!"
else
    if [ -n "$BACKEND_RUNNING" ]; then
        echo "⚠️  Backend still running on port 8001"
        echo "   Run: lsof -ti:8001 | xargs kill -9"
    fi
    if [ -n "$FRONTEND_RUNNING" ]; then
        echo "⚠️  Frontend still running on port 3000"
        echo "   Run: lsof -ti:3000 | xargs kill -9"
    fi
fi

echo "========================================"
