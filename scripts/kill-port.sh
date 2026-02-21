#!/bin/bash
# Kill process using a specific port
# Usage: ./kill-port.sh [PORT]
# Default port is 7860 (the port that needs to be freed before app starts on 7861)

PORT=${1:-7861}

echo "🔍 Checking for processes on port $PORT..."

# Find process using the port
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo "✅ No process found on port $PORT"
    exit 0
fi

echo "⚠️  Found process $PID using port $PORT"
echo "🔪 Killing process..."

kill -9 $PID

if [ $? -eq 0 ]; then
    echo "✅ Successfully killed process $PID"
    sleep 1
    
    # Verify it's dead
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo "❌ Process still running on port $PORT"
        exit 1
    else
        echo "✅ Port $PORT is now free"
        exit 0
    fi
else
    echo "❌ Failed to kill process $PID"
    exit 1
fi

# Made with Bob
