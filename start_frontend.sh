
#!/bin/bash

echo "========================================"
echo "Starting CMU-Africa Assistant Frontend"
echo "========================================"

cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start development server
echo "Starting React development server on http://localhost:3000"
echo "Press Ctrl+C to stop"
npm start
