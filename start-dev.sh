#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting RhymeslikeDimes Development Environment${NC}"

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}Port $1 is already in use!${NC}"
        return 1
    fi
    return 0
}

# Check ports
echo -e "${BLUE}Checking ports...${NC}"
if ! check_port 8001; then
    echo "Please free up port 8001 or change the backend port in config"
    exit 1
fi

if ! check_port 3000; then
    echo "Please free up port 3000 or change the frontend port in vite.config.ts"
    exit 1
fi

# Start backend
echo -e "${GREEN}Starting backend server on port 8001...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start backend in background
python app/main.py &
BACKEND_PID=$!

cd ..

# Start frontend
echo -e "${GREEN}Starting frontend development server on port 3000...${NC}"
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    npm install
fi

# Start frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo -e "${GREEN}Development servers started!${NC}"
echo -e "Backend API: http://localhost:8001"
echo -e "Frontend: http://localhost:3000"
echo -e "API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Servers stopped${NC}"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Wait for both processes
wait