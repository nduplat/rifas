#!/bin/bash

# Rifa1122 Backend Local Development Setup Script
# This script sets up the local development environment including:
# - Python virtual environment
# - Dependencies installation
# - Database setup and migrations
# - Initial data loading

set -e  # Exit on any error

echo "🚀 Starting Rifa1122 Backend Local Setup..."

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

# Check if we're in the right directory
if [ ! -f "backend/pyproject.toml" ]; then
    print_error "Please run this script from the project root directory (containing backend/ folder)"
    exit 1
fi

cd backend

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    print_error "Python 3.11 or higher is required. Current version: $python_version"
    exit 1
fi
print_success "Python version check passed: $python_version"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    print_error "Poetry is not installed. Please install Poetry first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi
print_success "Poetry is installed"

# Install dependencies
print_status "Installing Python dependencies with Poetry..."
poetry install
print_success "Dependencies installed"

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from .env.example..."
    cp .env.example .env
    print_warning "Please update .env file with your actual configuration values"
else
    print_success ".env file already exists"
fi

# Check if Docker is available for database setup
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_status "Docker and Docker Compose detected. Setting up database services..."

    # Start database services
    print_status "Starting PostgreSQL and Redis services..."
    docker-compose up -d postgres redis

    # Wait for PostgreSQL to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker-compose exec -T postgres pg_isready -U rifa_user -d rifa1122 &>/dev/null; then
            print_success "PostgreSQL is ready!"
            break
        fi
        print_status "Waiting for PostgreSQL... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done

    if [ $attempt -gt $max_attempts ]; then
        print_error "PostgreSQL failed to start within expected time"
        exit 1
    fi

    # Run database migrations
    print_status "Running database migrations..."
    poetry run alembic upgrade head
    print_success "Database migrations completed"

    # Load initial data
    print_status "Loading initial data..."
    poetry run python -c "
import json
import sys
import os
sys.path.append('.')

from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.models import *

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Load initial data
    with open('initial_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert loterias
    for loteria_data in data.get('loterias', []):
        loteria = Loteria(**loteria_data)
        db.merge(loteria)

    # Insert categorias
    for categoria_data in data.get('categorias', []):
        categoria = CategoriaRifa(**categoria_data)
        db.merge(categoria)

    # Insert rifas
    for rifa_data in data.get('rifas', []):
        rifa = Rifa(**rifa_data)
        db.merge(rifa)

    # Insert users
    for user_data in data.get('users', []):
        user = User(**user_data)
        db.merge(user)

    # Insert tickets
    for ticket_data in data.get('tickets', []):
        ticket = Ticket(**ticket_data)
        db.merge(ticket)

    # Insert ganadores
    for ganador_data in data.get('ganadores', []):
        ganador = Ganador(**ganador_data)
        db.merge(ganador)

    db.commit()
    print('Initial data loaded successfully!')

except Exception as e:
    print(f'Error loading initial data: {e}')
    db.rollback()
    sys.exit(1)
finally:
    db.close()
"
    print_success "Initial data loaded"

else
    print_warning "Docker not available. Please ensure you have PostgreSQL and Redis running manually."
    print_status "To run migrations manually:"
    echo "  cd backend"
    echo "  poetry run alembic upgrade head"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
print_success "Directories created"

# Run basic health check
print_status "Running basic health checks..."
if poetry run python -c "
import sys
sys.path.append('.')
try:
    from app.db.session import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Database connection: OK')
except Exception as e:
    print(f'Database connection: FAILED - {e}')
    sys.exit(1)
"; then
    print_success "Health checks passed"
else
    print_error "Health checks failed"
    exit 1
fi

print_success "🎉 Local development environment setup completed!"
echo ""
echo "Next steps:"
echo "1. Update your .env file with proper configuration"
echo "2. Start the development server:"
echo "   cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "3. Start Celery workers (in another terminal):"
echo "   cd backend && poetry run celery -A app.core.celery_app worker --loglevel=info"
echo "4. Access the API documentation at: http://localhost:8000/docs"
echo ""
echo "For production deployment:"
echo "1. Update production environment variables"
echo "2. Run: docker-compose -f docker-compose.yml up -d"
echo ""
print_warning "Remember to never commit .env files to version control!"