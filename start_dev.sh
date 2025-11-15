#!/bin/bash
# Start both frontend and backend servers for Diagrammatic

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "🚀 Starting Diagrammatic..."
echo ""

# Start backend in background
echo "▶️  Starting NLP backend on http://localhost:5000..."
npm run backend > /tmp/diagrammatic_backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Give backend a moment to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Failed to start backend. Check /tmp/diagrammatic_backend.log"
    exit 1
fi

echo "✓ Backend started"
echo ""

# Start frontend
echo "▶️  Starting frontend dev server on http://localhost:5173..."
npm run dev > /tmp/diagrammatic_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# Give frontend a moment to start
sleep 2

echo "✓ Frontend started"
echo ""

# Save PIDs to a file for stopping later
echo "$BACKEND_PID" > /tmp/diagrammatic_pids.txt
echo "$FRONTEND_PID" >> /tmp/diagrammatic_pids.txt

echo "═══════════════════════════════════════════════════════"
echo "✓ Diagrammatic is running!"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:5000"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/diagrammatic_backend.log"
echo "  Frontend: tail -f /tmp/diagrammatic_frontend.log"
echo ""
echo "To stop both servers, run: ./stop_dev.sh"
echo "═══════════════════════════════════════════════════════"
echo ""

# Keep script running and handle Ctrl+C
trap "echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Done'; exit 0" INT TERM

wait $BACKEND_PID $FRONTEND_PID
