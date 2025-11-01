#!/bin/bash

# Rifa1122 Celery Worker Runner Script
# This script starts Celery workers for processing background tasks
# including raffle closing, winner selection, and payout processing

set -e  # Exit on any error

echo "🚀 Starting Rifa1122 Celery Workers..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default configuration
WORKER_CONCURRENCY=${CELERY_CONCURRENCY:-4}
LOG_LEVEL=${CELERY_LOG_LEVEL:-info}
QUEUES=${CELERY_QUEUES:-celery}
WORKER_NAME=${CELERY_WORKER_NAME:-rifa1122_worker}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --concurrency=*)
            WORKER_CONCURRENCY="${1#*=}"
            shift
            ;;
        --log-level=*)
            LOG_LEVEL="${1#*=}"
            shift
            ;;
        --queues=*)
            QUEUES="${1#*=}"
            shift
            ;;
        --name=*)
            WORKER_NAME="${1#*=}"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --concurrency=N    Number of worker processes (default: 4)"
            echo "  --log-level=LEVEL  Logging level (default: info)"
            echo "  --queues=QUEUES   Queues to consume from (default: celery)"
            echo "  --name=NAME        Worker name prefix (default: rifa1122_worker)"
            echo "  --help             Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  CELERY_CONCURRENCY    Same as --concurrency"
            echo "  CELERY_LOG_LEVEL      Same as --log-level"
            echo "  CELERY_QUEUES         Same as --queues"
            echo "  CELERY_WORKER_NAME    Same as --name"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if we're in the right directory
if [ ! -f "backend/pyproject.toml" ]; then
    print_error "Please run this script from the project root directory (containing backend/ folder)"
    exit 1
fi

cd backend

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    print_error "Poetry is not installed. Please install Poetry first."
    exit 1
fi

# Check if Redis is running (required for Celery)
print_status "Checking Redis connectivity..."
if command -v redis-cli &> /dev/null; then
    if ! redis-cli ping &> /dev/null; then
        print_warning "Redis is not running locally. Make sure Redis is available."
        print_status "If using Docker, ensure the Redis container is running:"
        echo "  docker-compose up -d redis"
    else
        print_success "Redis is running"
    fi
else
    print_warning "redis-cli not found. Assuming Redis is available via Docker or remote connection."
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_warning "Virtual environment not found. Running init script first..."
    if [ -f "../scripts/init_local.sh" ]; then
        print_status "Running initialization script..."
        bash ../scripts/init_local.sh
    else
        print_error "Initialization script not found. Please run setup first."
        exit 1
    fi
fi

# Set environment variables for Celery
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down Celery workers..."
    # Kill any child processes
    pkill -P $$ 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

print_status "Starting Celery worker with the following configuration:"
echo "  Worker Name: $WORKER_NAME"
echo "  Concurrency: $WORKER_CONCURRENCY"
echo "  Log Level: $LOG_LEVEL"
echo "  Queues: $QUEUES"
echo ""

# Start Celery worker
print_status "Launching Celery worker..."
poetry run celery -A app.core.celery_app worker \
    --loglevel=$LOG_LEVEL \
    --concurrency=$WORKER_CONCURRENCY \
    --queues=$QUEUES \
    --hostname=$WORKER_NAME@%h \
    --pool=prefork \
    --max-tasks-per-child=1000 \
    --time-limit=3600 \
    --soft-time-limit=3300 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat

print_success "Celery worker started successfully"