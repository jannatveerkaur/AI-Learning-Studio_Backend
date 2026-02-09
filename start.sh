#!/bin/bash

# SmartLearn AI - Quick Start Script
# Run both backend and frontend in one command

echo "🚀 Starting SmartLearn AI..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found!${NC}"
    echo "Creating .env file. Please add your OpenAI API key."
    echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
    echo ""
fi

# Start backend in background
echo -e "${BLUE}📡 Starting Backend (FastAPI)...${NC}"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Logs: tail -f backend.log"
sleep 3

# Check if backend started
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Backend running at http://localhost:8000${NC}"
else
    echo -e "${YELLOW}❌ Backend failed to start. Check backend.log${NC}"
    exit 1
fi

# Start frontend
echo ""
echo -e "${BLUE}🎨 Starting Frontend (React)...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies (first time only)..."
    npm install
fi

echo ""
echo -e "${GREEN}✅ Starting React development server...${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 SmartLearn AI is running!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Frontend:${NC}  http://localhost:3000"
echo -e "${BLUE}Backend:${NC}   http://localhost:8000"
echo -e "${BLUE}API Docs:${NC}  http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop both servers"
echo ""

npm start
