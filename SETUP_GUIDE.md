# Rifa1122 Setup Guide

This guide provides comprehensive instructions for setting up both the backend API and Flutter frontend of the Rifa1122 lottery system.

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.11 or higher
- **Flutter**: 3.9.2 or higher
- **Docker**: 20.10+ (recommended for backend)
- **Docker Compose**: 2.0+ (recommended for backend)
- **Git**: 2.25+ for version control

### Development Tools

- **VS Code** (recommended) with Flutter and Python extensions
- **Git Bash** (Windows) or Terminal (macOS/Linux)
- **Postman** or similar API testing tool (optional)

## Backend Setup

### Option 1: Docker Setup (Recommended)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Update environment variables in `.env`:**
   ```env
   SECRET_KEY=your-super-secret-jwt-key-here
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   DEBUG=true
   ```

4. **Run the automated setup script:**
   ```bash
   chmod +x ../scripts/init_local.sh
   ../scripts/init_local.sh
   ```

   This script will:
   - Install Python dependencies with Poetry
   - Start PostgreSQL and Redis containers
   - Run database migrations
   - Load initial data
   - Create necessary directories

5. **Start the development server:**
   ```bash
   docker-compose up -d
   ```

6. **Verify setup:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Flower (Celery monitoring): http://localhost:5555
   - pgAdmin: http://localhost:5050

### Option 2: Manual Setup

1. **Install Poetry (Python dependency manager):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   poetry install
   ```

3. **Set up PostgreSQL and Redis:**
   - Install PostgreSQL 15+ locally or use a cloud instance
   - Install Redis 7+ locally or use a cloud instance
   - Create database: `rifa1122`
   - Create user: `rifa_user` with password `rifa_password`

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URLs and secrets
   ```

5. **Run database migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

6. **Load initial data:**
   ```bash
   poetry run python -c "
   import json
   import sys
   sys.path.append('.')
   from sqlalchemy.orm import sessionmaker
   from app.db.session import engine
   from app.models import *

   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   db = SessionLocal()

   with open('initial_data.json', 'r', encoding='utf-8') as f:
       data = json.load(f)

   # Load loterias, categorias, rifas, users, tickets, ganadores
   # ... (same as in init_local.sh)

   db.commit()
   db.close()
   print('Initial data loaded successfully!')
   "
   ```

7. **Start the server:**
   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Start Celery workers (in another terminal):**
   ```bash
   poetry run celery -A app.core.celery_app worker --loglevel=info
   ```

## Frontend Setup (Flutter)

### 1. Install Flutter

**Windows:**
1. Download Flutter SDK from https://flutter.dev/docs/get-started/install/windows
2. Extract to `C:\flutter`
3. Add `C:\flutter\bin` to PATH
4. Run `flutter doctor` to verify installation

**macOS:**
1. Download Flutter SDK from https://flutter.dev/docs/get-started/install/macos
2. Extract to `~/flutter`
3. Add to PATH: `export PATH="$PATH:~/flutter/bin"`
4. Run `flutter doctor` to verify installation

**Linux:**
1. Download Flutter SDK from https://flutter.dev/docs/get-started/install/linux
2. Extract and add to PATH
3. Run `flutter doctor` to verify installation

### 2. Set up the project

1. **Navigate to Flutter project:**
   ```bash
   cd rifa1122
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Generate code (for Freezed models):**
   ```bash
   flutter pub run build_runner build
   ```

4. **Configure API endpoint (optional):**
   - Open `lib/core/network/api_service.dart`
   - Update `baseUrl` if needed (default: `http://localhost:8000/api/v1`)

### 3. Run the application

**For Android:**
```bash
flutter run
```
Select an Android device/emulator when prompted.

**For iOS (macOS only):**
```bash
flutter run
```
Select an iOS simulator when prompted.

**For Web:**
```bash
flutter run -d chrome
```

**For Desktop (Windows/macOS/Linux):**
```bash
flutter run -d windows  # or macos/linux
```

## Testing the Setup

### Backend Tests

1. **Run unit tests:**
   ```bash
   cd backend
   poetry run pytest app/tests/unit/ -v
   ```

2. **Run integration tests:**
   ```bash
   poetry run pytest app/tests/integration/ -v
   ```

3. **Run all tests:**
   ```bash
   poetry run pytest --cov=app --cov-report=html
   ```

### API Testing

1. **Access Swagger UI:**
   - Open http://localhost:8000/docs
   - Test authentication endpoints first

2. **Test user registration:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
        -H "Content-Type: application/json" \
        -d '{
          "nombre": "Test User",
          "email": "test@example.com",
          "password": "test123",
          "rol": "jugador"
        }'
   ```

3. **Test login:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=test@example.com&password=test123"
   ```

### Flutter Tests

1. **Run widget tests:**
   ```bash
   cd rifa1122
   flutter test
   ```

2. **Run integration tests:**
   ```bash
   flutter test integration_test/
   ```

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://rifa_user:rifa_password@postgres:5432/rifa1122` | Yes |
| `REDIS_HOST` | Redis host | `redis` | Yes |
| `REDIS_PORT` | Redis port | `6379` | Yes |
| `SECRET_KEY` | JWT secret key | - | Yes |
| `STRIPE_SECRET_KEY` | Stripe secret key | - | Yes (for payments) |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | - | Yes (for payments) |
| `DEBUG` | Debug mode | `false` | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | `30` | No |

### Flutter Configuration

The Flutter app uses mock services by default. To connect to the real backend:

1. Update `lib/core/network/api_service.dart`:
   ```dart
   class ApiService {
     static const String baseUrl = 'http://localhost:8000/api/v1';
     // ... rest of configuration
   }
   ```

2. For production, update the base URL to your deployed backend URL.

## Troubleshooting

### Common Backend Issues

**Database connection failed:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists and user has permissions

**Redis connection failed:**
- Ensure Redis is running on correct port
- Check REDIS_HOST and REDIS_PORT

**Port 8000 already in use:**
- Kill process using port: `lsof -ti:8000 | xargs kill -9`
- Or change port in uvicorn command

**Migration errors:**
- Reset database: `poetry run alembic downgrade base`
- Then run: `poetry run alembic upgrade head`

### Common Flutter Issues

**Flutter doctor shows issues:**
- Install missing Android SDK components
- Accept Android licenses: `flutter doctor --android-licenses`
- Install Xcode command line tools (macOS)

**Build fails:**
- Clean and rebuild: `flutter clean && flutter pub get`
- Regenerate Freezed code: `flutter pub run build_runner build --delete-conflicting-outputs`

**iOS build fails:**
- Run `pod install` in `ios/` directory
- Ensure CocoaPods is installed: `sudo gem install cocoapods`

**Android build fails:**
- Ensure Android SDK is properly configured
- Check Android Studio SDK location

### Network Issues

**CORS errors:**
- Backend is configured to allow requests from Flutter apps
- For web development, ensure CORS is properly configured

**Connection refused:**
- Ensure backend is running on correct port
- Check firewall settings
- For mobile emulators, use `10.0.2.2` instead of `localhost`

## Development Workflow

### Backend Development

1. **Make code changes**
2. **Run tests:** `poetry run pytest`
3. **Check code quality:** `poetry run black . && poetry run isort .`
4. **Restart server if needed**

### Flutter Development

1. **Make code changes**
2. **Hot reload:** Press `r` in terminal or use IDE
3. **Run tests:** `flutter test`
4. **Build APK/IPA:** `flutter build apk` or `flutter build ios`

## Next Steps

After successful setup:

1. **Explore the API documentation** at http://localhost:8000/docs
2. **Test the Flutter app** on your device/emulator
3. **Review the project structure** and understand the architecture
4. **Start developing** new features or customizing existing ones

For production deployment, see the [Deployment Guide](DEPLOYMENT_GUIDE.md).