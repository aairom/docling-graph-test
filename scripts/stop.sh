#!/bin/bash
# Stop script for Docling-Graph Showcase Application

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
PORT=7860

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Docling-Graph Showcase Stopper${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Kill any process on port 7860
echo -e "${BLUE}🔍 Checking for processes on port ${PORT}...${NC}"
PORT_PID=$(lsof -ti:${PORT} 2>/dev/null || true)

if [ -n "${PORT_PID}" ]; then
    echo -e "${YELLOW}⚠️  Found process ${PORT_PID} using port ${PORT}${NC}"
    echo -e "${BLUE}🔪 Killing process on port ${PORT}...${NC}"
    kill -9 ${PORT_PID} 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}✓${NC} Port ${PORT} is now free"
else
    echo -e "${GREEN}✓${NC} No process found on port ${PORT}"
fi

# Check if PID file exists
if [ ! -f "${PID_FILE}" ]; then
    echo -e "${YELLOW}⚠️  Application is not running (no PID file found)${NC}"
    exit 0
fi

# Read PID
PID=$(cat "${PID_FILE}")

# Check if process is running
if ! ps -p "${PID}" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Application is not running (PID ${PID} not found)${NC}"
    rm -f "${PID_FILE}"
    exit 0
fi

# Stop the application
echo -e "${BLUE}🛑 Stopping application (PID: ${PID})...${NC}"

kill "${PID}"

# Wait for process to stop
TIMEOUT=10
COUNTER=0

while ps -p "${PID}" > /dev/null 2>&1; do
    sleep 1
    COUNTER=$((COUNTER + 1))
    
    if [ ${COUNTER} -ge ${TIMEOUT} ]; then
        echo -e "${YELLOW}⚠️  Process did not stop gracefully, forcing...${NC}"
        kill -9 "${PID}" 2>/dev/null || true
        break
    fi
done

# Remove PID file
rm -f "${PID_FILE}"

echo -e "${GREEN}✓${NC} Application stopped successfully"
echo ""

# Made with Bob
