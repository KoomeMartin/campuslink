#!/bin/bash

echo "========================================"
echo "CMU-Africa Assistant - Service Status"
echo "========================================"
echo ""

# Check backend
echo "🔍 Checking Backend (port 8001)..."
BACKEND_PID=$(lsof -ti:8001 2>/dev/null)
if [ -n "$BACKEND_PID" ]; then
    echo "✅ Backend is RUNNING (PID: $BACKEND_PID)"
    echo "   URL: http://localhost:8001"
    echo "   Docs: http://localhost:8001/docs"
    
    # Try to get health status
    HEALTH=$(curl -s http://localhost:8001/api/health 2>/dev/null)
    if [ -n "$HEALTH" ]; then
        echo "   Health: $(echo $HEALTH | jq -r '.status' 2>/dev/null || echo 'OK')"
    fi
else
    echo "❌ Backend is NOT running"
    echo "   Start with: ./start_backend.sh"
fi

echo ""

# Check frontend
echo "🔍 Checking Frontend (port 3000)..."
FRONTEND_PID=$(lsof -ti:3000 2>/dev/null)
if [ -n "$FRONTEND_PID" ]; then
    echo "✅ Frontend is RUNNING (PID: $FRONTEND_PID)"
    echo "   URL: http://localhost:3000"
else
    echo "❌ Frontend is NOT running"
    echo "   Start with: ./start_frontend.sh"
fi

echo ""

# Overall status
if [ -n "$BACKEND_PID" ] && [ -n "$FRONTEND_PID" ]; then
    echo "🎉 System Status: FULLY OPERATIONAL"
    echo ""
    echo "📱 Access the application at:"
    echo "   👉 http://localhost:3000"
elif [ -n "$BACKEND_PID" ]; then
    echo "⚠️  System Status: PARTIAL (Backend only)"
    echo "   Start frontend: ./start_frontend.sh"
elif [ -n "$FRONTEND_PID" ]; then
    echo "⚠️  System Status: PARTIAL (Frontend only)"
    echo "   Start backend: ./start_backend.sh"
else
    echo "❌ System Status: NOT RUNNING"
    echo ""
    echo "To start all services:"
    echo "   Terminal 1: ./start_backend.sh"
    echo "   Terminal 2: ./start_frontend.sh"
fi

echo "========================================"
