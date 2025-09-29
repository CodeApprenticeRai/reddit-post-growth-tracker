#!/bin/bash

# Parse command line arguments
FRONTEND_MODE="dev"  # Default to development mode
BUILD_FRONTEND=false
START_FRONTEND=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --frontend)
            FRONTEND_MODE="$2"
            shift 2
            ;;
        --build-frontend)
            BUILD_FRONTEND=true
            shift
            ;;
        --start-frontend)
            START_FRONTEND=true
            shift
            ;;
        --help)
            echo "Reddit Post Growth Tracker Startup Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --frontend MODE       Frontend mode: dev, prod, or none (default: dev)"
            echo "  --build-frontend      Build frontend for production"
            echo "  --start-frontend      Start frontend development server"
            echo "  --help               Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Start backend only"
            echo "  $0 --start-frontend          # Start backend + frontend dev server"
            echo "  $0 --build-frontend          # Build frontend + start backend"
            echo "  $0 --frontend prod           # Production mode (builds frontend)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check for Reddit API credentials
echo "🔐 Checking Reddit API credentials..."

# Check for .env file first
if [ -f ".env" ]; then
    echo "📄 Found .env file, loading environment variables..."
    # Load environment variables from .env file
    export $(grep -v '^#' .env | xargs)
    
    # Check if required variables are set
    if [ -z "$REDDIT_CLIENT_ID" ] || [ -z "$REDDIT_CLIENT_SECRET" ]; then
        echo "❌ Error: Missing Reddit API credentials in .env file!"
        echo "Please add the following to your .env file:"
        echo "REDDIT_CLIENT_ID=your_reddit_client_id"
        echo "REDDIT_CLIENT_SECRET=your_reddit_client_secret"
        echo "REDDIT_USER_AGENT=RedditPostGrowthTracker/1.0"
        exit 1
    fi
    
    echo "✅ Reddit API credentials loaded from .env file"
    
# Fallback to config.json if .env doesn't exist
elif [ -f "config.json" ]; then
    echo "📄 Found config.json file (consider migrating to .env for better security)"
    echo "✅ Using config.json for Reddit API credentials"
    
else
    echo "❌ Error: No Reddit API credentials found!"
    echo ""
    echo "Please create a .env file with your Reddit API credentials:"
    echo "REDDIT_CLIENT_ID=your_reddit_client_id"
    echo "REDDIT_CLIENT_SECRET=your_reddit_client_secret"
    echo "REDDIT_USER_AGENT=RedditPostGrowthTracker/1.0"
    echo ""
    echo "Or create a config.json file:"
    echo '{'
    echo '  "client_id": "your_reddit_client_id",'
    echo '  "client_secret": "your_reddit_client_secret",'
    echo '  "user_agent": "RedditPostGrowthTracker/1.0"'
    echo '}'
    exit 1
fi

# Install Python dependencies if needed
echo "📦 Checking Python dependencies..."

# Function to find pipenv command
find_pipenv() {
    # Check if pipenv is in PATH
    if command -v pipenv &> /dev/null; then
        echo "pipenv"
        return 0
    fi
    
    # Check common installation locations
    local common_paths=(
        "$HOME/.local/bin/pipenv"
        "$HOME/Library/Python/*/bin/pipenv"
        "/usr/local/bin/pipenv"
        "/opt/homebrew/bin/pipenv"
    )
    
    for path_pattern in "${common_paths[@]}"; do
        for path in $path_pattern; do
            if [ -f "$path" ]; then
                echo "$path"
                return 0
            fi
        done
    done
    
    return 1
}

PIPENV_CMD=$(find_pipenv)

if [ $? -eq 0 ]; then
    echo "🔧 Installing Python dependencies with pipenv..."
    echo "Using pipenv at: $PIPENV_CMD"
    $PIPENV_CMD install --python python3
    PYTHON_CMD="$PIPENV_CMD run python"
else
    echo "⚠️  pipenv not found, using system python3"
    echo "💡 Consider installing pipenv: pip install pipenv"
    echo "   Or: pip install --user pipenv"
    PYTHON_CMD="python3"
fi

# Initialize database if needed
if [ ! -f "db/data.db" ]; then
    echo "📊 Initializing database..."
    $PYTHON_CMD init_db.py
fi

# Start the Flask server in background
echo "🌐 Starting Flask server..."
$PYTHON_CMD app.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Start the background service
echo "🔄 Starting background data collection service..."
$PYTHON_CMD tracker_service.py &
SERVICE_PID=$!

# Handle frontend based on mode
FRONTEND_PID=""
if [ "$FRONTEND_MODE" = "prod" ] || [ "$BUILD_FRONTEND" = true ] || [ "$START_FRONTEND" = true ] || [ "$FRONTEND_MODE" = "dev" ]; then
    if [ -f "package.json" ]; then
        # Check if node_modules exists, if not install dependencies
        if [ ! -d "node_modules" ]; then
            echo "📦 Installing frontend dependencies..."
            npm install
            if [ $? -eq 0 ]; then
                echo "✅ Frontend dependencies installed successfully!"
            else
                echo "❌ Failed to install frontend dependencies"
                echo "⚠️  Skipping frontend operations"
                FRONTEND_MODE="none"
            fi
        else
            echo "✅ Frontend dependencies already installed"
        fi
        
        # Build frontend if in production mode
        if [ "$FRONTEND_MODE" = "prod" ] || [ "$BUILD_FRONTEND" = true ]; then
            echo "🏗️  Building frontend for production..."
            npm run build
            if [ $? -eq 0 ]; then
                echo "✅ Frontend built successfully!"
            else
                echo "❌ Frontend build failed"
            fi
        fi
        
        # Start frontend development server
        if [ "$START_FRONTEND" = true ] || [ "$FRONTEND_MODE" = "dev" ]; then
            echo "🌐 Starting frontend development server..."
            npm start &
            FRONTEND_PID=$!
            echo "✅ Frontend development server started (PID: $FRONTEND_PID)"
        fi
    else
        echo "⚠️  No package.json found, skipping frontend operations"
    fi
fi

echo ""
echo "✅ Application started successfully!"
echo "🔗 Backend API: http://localhost:5000"
echo "📊 Background service: Running (PID: $SERVICE_PID)"

if [ -n "$FRONTEND_PID" ]; then
    echo "📱 Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
elif [ "$FRONTEND_MODE" = "prod" ] || [ "$BUILD_FRONTEND" = true ]; then
    echo "📱 Frontend: Built and ready to serve"
else
    echo "📱 Frontend: Not started (use --start-frontend to start dev server)"
fi

echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $SERVER_PID 2>/dev/null
    kill $SERVICE_PID 2>/dev/null
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
