#!/bin/bash
# Stop both frontend and backend servers for Diagrammatic

echo "🛑 Stopping Diagrammatic..."
echo ""

if [ -f /tmp/diagrammatic_pids.txt ]; then
    PIDs=$(cat /tmp/diagrammatic_pids.txt)
    count=0
    for PID in $PIDs; do
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            count=$((count + 1))
            echo "✓ Killed process $PID"
        fi
    done

    if [ $count -gt 0 ]; then
        rm /tmp/diagrammatic_pids.txt
        echo ""
        echo "✓ All servers stopped"
    else
        echo "⚠️  No running processes found"
    fi
else
    echo "⚠️  No PID file found. Trying to kill by port..."

    # Try killing by port (macOS specific)
    if command -v lsof &> /dev/null; then
        # Kill backend
        lsof -ti :5000 | xargs kill -9 2>/dev/null && echo "✓ Killed backend (port 5000)" || true

        # Kill frontend
        lsof -ti :5173 | xargs kill -9 2>/dev/null && echo "✓ Killed frontend (port 5173)" || true
    else
        echo "❌ Cannot find running processes. Please kill manually:"
        echo "   Backend: sudo lsof -ti :5000 | xargs kill -9"
        echo "   Frontend: sudo lsof -ti :5173 | xargs kill -9"
        exit 1
    fi
fi

echo ""
echo "Logs saved to:"
echo "  /tmp/diagrammatic_backend.log"
echo "  /tmp/diagrammatic_frontend.log"
