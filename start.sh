#!/bin/bash

# Reddit Post Growth Tracker Startup Script

echo "🚀 Starting Reddit Post Growth Tracker..."

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "❌ Error: config.json not found!"
    echo "Please create config.json with your Reddit API credentials:"
    echo '{'
    echo '  "client_id": "your_reddit_client_id",'
    echo '  "client_secret": "your_reddit_client_secret",'
    echo '  "user_agent": "RedditPostGrowthTracker/1.0"'
    echo '}'
    exit 1
fi

# Initialize database if needed
if [ ! -f "db/data.db" ]; then
    echo "📊 Initializing database..."
    python3 init_db.py
fi

# Start the Flask server in background
echo "🌐 Starting Flask server..."
python3 app.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Start the background service
echo "🔄 Starting background data collection service..."
python3 tracker_service.py &
SERVICE_PID=$!

echo "✅ Application started successfully!"
echo "📱 Frontend: http://localhost:3000 (run 'npm start' in another terminal)"
echo "🔗 Backend API: http://localhost:5000"
echo "📊 Background service: Running (PID: $SERVICE_PID)"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $SERVER_PID 2>/dev/null
    kill $SERVICE_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
