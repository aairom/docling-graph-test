#!/bin/bash
# Launch script for Docling-Graph Showcase Application
# Starts the application in detached mode

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="docling-graph-app"
LOG_DIR="logs"
PID_FILE="${LOG_DIR}/${APP_NAME}.pid"
LOG_FILE="${LOG_DIR}/${APP_NAME}.log"
PORT=7861

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Docling-Graph Showcase Launcher${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create logs directory
mkdir -p "${LOG_DIR}"

# Check if already running
if [ -f "${PID_FILE}" ]; then
    PID=$(cat "${PID_FILE}")
    if ps -p "${PID}" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Application is already running (PID: ${PID})${NC}"
        echo -e "${YELLOW}   Access at: http://localhost:${PORT}${NC}"
        echo ""
        echo -e "To stop: ${GREEN}./scripts/stop.sh${NC}"
        exit 1
    else
        echo -e "${YELLOW}⚠️  Stale PID file found, removing...${NC}"
        rm -f "${PID_FILE}"
    fi
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo -e "   Please install Python 3.10 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "   Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Check and install dependencies
echo ""
echo -e "${BLUE}📦 Checking dependencies...${NC}"

if ! python -c "import gradio" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${GREEN}✓${NC} Dependencies already installed"
fi

# Check Ollama
echo ""
echo -e "${BLUE}🤖 Checking Ollama...${NC}"

if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo -e "   Install from: https://ollama.com"
    echo -e "   Or run: curl -fsSL https://ollama.com/install.sh | sh"
else
    echo -e "${GREEN}✓${NC} Ollama found: $(ollama --version 2>/dev/null || echo 'installed')"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama service is running"
        
        # Check for granite model
        if ollama list 2>/dev/null | grep -q "granite4"; then
            echo -e "${GREEN}✓${NC} Granite4 model available"
        else
            echo -e "${YELLOW}⚠️  Granite4 model not found${NC}"
            echo -e "   Pulling granite4 (this may take a few minutes)..."
            ollama pull granite4
            echo -e "${GREEN}✓${NC} Granite4 model ready"
        fi
    else
        echo -e "${YELLOW}⚠️  Ollama service not running${NC}"
        echo -e "   Starting Ollama in background..."
        nohup ollama serve > "${LOG_DIR}/ollama.log" 2>&1 &
        sleep 3
        
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} Ollama service started"
        else
            echo -e "${RED}❌ Failed to start Ollama${NC}"
            echo -e "   Please start manually: ollama serve"
        fi
    fi
fi

# Create necessary directories
echo ""
echo -e "${BLUE}📁 Setting up directories...${NC}"
mkdir -p input output
echo -e "${GREEN}✓${NC} Directories ready"

# Start the application
echo ""
echo -e "${BLUE}🚀 Starting application...${NC}"

# Start in background
nohup python3 app.py > "${LOG_FILE}" 2>&1 &
APP_PID=$!

# Save PID
echo "${APP_PID}" > "${PID_FILE}"

# Wait a moment and check if it's running
sleep 3

if ps -p "${APP_PID}" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Application started successfully!"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Application Running${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "  ${BLUE}URL:${NC}     http://localhost:${PORT}"
    echo -e "  ${BLUE}PID:${NC}     ${APP_PID}"
    echo -e "  ${BLUE}Logs:${NC}    ${LOG_FILE}"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  View logs:  ${GREEN}tail -f ${LOG_FILE}${NC}"
    echo -e "  Stop app:   ${GREEN}./scripts/stop.sh${NC}"
    echo ""
else
    echo -e "${RED}❌ Failed to start application${NC}"
    echo -e "   Check logs: ${LOG_FILE}"
    rm -f "${PID_FILE}"
    exit 1
fi

# Made with Bob
