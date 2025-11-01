# Developer Onboarding Guide

Welcome to the Rifa1122 development team! This guide will help you get up and running with the lottery and raffle management system quickly and efficiently.

## 🎯 Quick Start (15 minutes)

### Prerequisites Check
- [ ] Python 3.11+ installed
- [ ] Flutter 3.9.2+ installed
- [ ] Docker and Docker Compose installed
- [ ] Git configured
- [ ] VS Code with Flutter and Python extensions

### Get the Code
```bash
git clone https://github.com/your-org/rifa1122.git
cd rifa1122
```

### Backend Setup (5 minutes)
```bash
cd backend
cp .env.example .env
# Edit .env with your secrets
chmod +x ../scripts/init_local.sh
../scripts/init_local.sh
```

### Frontend Setup (5 minutes)
```bash
cd ../rifa1122
flutter pub get
flutter pub run build_runner build
```

### Start Developing
```bash
# Terminal 1: Backend
cd backend && docker-compose up -d

# Terminal 2: Frontend
cd rifa1122 && flutter run
```

**You're done!** 🎉 Visit http://localhost:8000/docs for API docs and start the Flutter app.

---

## 📚 Understanding the System

### What is Rifa1122?

Rifa1122 is a comprehensive lottery and raffle management system designed for the Colombian market. It allows users to participate in raffles based on official lottery results, with features like:

- **Multi-tier raffle categories** (Bronce, Plata, Oro, etc.)
- **Automated winner selection** based on lottery results
- **Stripe payment integration**
- **Real-time notifications**
- **AI-powered recommendations**
- **Admin dashboard** for raffle management

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flutter App   │    │   FastAPI        │    │   PostgreSQL    │
│                 │◄──►│   Backend        │◄──►│   Database      │
│ - Mobile/Web    │    │                 │    │                 │
│ - User Interface│    │ - REST API       │    │ - Users         │
│ - State Mgmt    │    │ - Auth/JWT       │    │ - Raffles       │
└─────────────────┘    │ - Webhooks       │    │ - Tickets       │
                       └─────────────────┘    │ - Transactions   │
                               ▲             └─────────────────┘
                               │
                       ┌─────────────────┐
                       │     Redis       │
                       │                 │
                       │ - Cache         │
                       │ - Celery Broker │
                       └─────────────────┘
                               ▲
                               │
                       ┌─────────────────┐
                       │    Celery       │
                       │   Workers       │
                       │                 │
                       │ - Winner Select │
                       │ - Payouts       │
                       │ - Notifications │
                       └─────────────────┘
```

### Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI (Python) | REST API, async operations |
| **Database** | PostgreSQL | Persistent data storage |
| **Cache/Broker** | Redis | Caching, message queuing |
| **Workers** | Celery | Background tasks |
| **Frontend** | Flutter | Cross-platform mobile/web app |
| **Payments** | Stripe | Payment processing |
| **Deployment** | Docker | Containerization |

---

## 🏗️ Development Workflow

### 1. Choose Your Task

**New Features:**
- Check the [Project Board](https://github.com/your-org/rifa1122/projects) for assigned issues
- Review requirements and acceptance criteria
- Create a feature branch: `git checkout -b feature/your-feature-name`

**Bug Fixes:**
- Reproduce the issue locally
- Create a bugfix branch: `git checkout -b bugfix/issue-description`

### 2. Development Process

#### Backend Development
```bash
# Activate virtual environment
cd backend
poetry shell

# Run tests before changes
poetry run pytest app/tests/unit/ -v

# Make your changes
# ... edit code ...

# Run tests after changes
poetry run pytest app/tests/unit/ -v

# Format code
poetry run black .
poetry run isort .

# Test integration
poetry run pytest app/tests/integration/ -v
```

#### Frontend Development
```bash
cd rifa1122

# Run tests
flutter test

# Format code
flutter format .

# Analyze code
flutter analyze

# Run on device
flutter run
```

### 3. Code Quality Standards

#### Python (Backend)
- **Linting:** `ruff` and `black` for code formatting
- **Type hints:** Required for all functions
- **Docstrings:** Use Google-style docstrings
- **Testing:** Minimum 80% coverage required

#### Dart (Frontend)
- **Linting:** `flutter analyze` must pass
- **Formatting:** `flutter format` required
- **Testing:** Widget and unit tests required
- **State management:** Use Riverpod for all state

### 4. Database Changes

**For schema changes:**
1. Create migration: `alembic revision -m "your change description"`
2. Edit the migration file
3. Test migration: `alembic upgrade head`
4. Update models if needed

**For data changes:**
1. Update `initial_data.json` if it's seed data
2. Create data migration script if needed

### 5. Testing Strategy

#### Backend Testing
```bash
# Unit tests
poetry run pytest app/tests/unit/ -v

# Integration tests
poetry run pytest app/tests/integration/ -v

# End-to-end tests
poetry run pytest app/tests/e2e/ -v

# With coverage
poetry run pytest --cov=app --cov-report=html
```

#### Frontend Testing
```bash
# Unit tests
flutter test test/

# Widget tests
flutter test test/widget_test.dart

# Integration tests
flutter test integration_test/
```

### 6. Commit and Push

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication flow

- Implement JWT token generation
- Add login/register endpoints
- Update user model with password hashing
- Add comprehensive tests"

# Push to your branch
git push origin feature/your-feature-name
```

### 7. Create Pull Request

1. **Go to GitHub** and create a PR
2. **Fill out the PR template:**
   - Description of changes
   - Screenshots/videos if UI changes
   - Testing instructions
   - Breaking changes (if any)

3. **Request review** from team members
4. **Address feedback** and update PR
5. **Merge when approved**

---

## 🔧 Development Tools & Tips

### Essential VS Code Extensions

**For Flutter:**
- Flutter
- Dart
- Awesome Flutter Snippets

**For Python:**
- Python
- Pylance
- Python Docstring Generator

**General:**
- GitLens
- Bracket Pair Colorizer
- Prettier

### Useful Commands

#### Backend
```bash
# Start development server
poetry run uvicorn app.main:app --reload

# Start Celery workers
poetry run celery -A app.core.celery_app worker --loglevel=info

# Run database migrations
poetry run alembic upgrade head

# Create new migration
poetry run alembic revision -m "description"

# Format code
poetry run black . && poetry run isort .
```

#### Frontend
```bash
# Generate Freezed models
flutter pub run build_runner build

# Clean and rebuild
flutter clean && flutter pub get

# Run on specific device
flutter devices  # List devices
flutter run -d <device-id>

# Build for production
flutter build apk  # Android
flutter build ios  # iOS
flutter build web  # Web
```

#### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up -d --build api
```

### Debugging Tips

#### Backend Debugging
- Use `print()` statements or `logging.debug()`
- Check API logs: `docker-compose logs api`
- Use PDB: `import pdb; pdb.set_trace()`
- Test endpoints with curl/Postman

#### Frontend Debugging
- Use `print()` or `debugPrint()` statements
- Flutter DevTools for widget inspection
- Hot reload for quick iteration
- Check device logs with `flutter logs`

#### Database Debugging
- Use pgAdmin to inspect data
- Check migration status: `alembic current`
- View raw SQL queries in logs

---

## 📋 Code Organization

### Backend Structure
```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/     # API route handlers
│   │   └── api.py         # API router configuration
│   ├── core/              # Core functionality
│   │   ├── config.py      # Settings
│   │   ├── security.py    # Auth utilities
│   │   └── celery_app.py  # Background tasks
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── db/                # Database setup
├── tests/                 # Test suites
├── alembic/               # Database migrations
└── scripts/               # Utility scripts
```

### Frontend Structure
```
rifa1122/
├── lib/
│   ├── core/              # Core functionality
│   │   ├── network/       # API clients
│   │   ├── theme/         # UI themes
│   │   └── utils/         # Utilities
│   ├── features/          # Feature modules
│   │   ├── auth/          # Authentication
│   │   ├── rifas/         # Raffles
│   │   └── tickets/       # Tickets
│   └── main.dart          # App entry point
├── test/                  # Unit tests
├── integration_test/      # Integration tests
└── android/ios/web/       # Platform-specific code
```

---

## 🚨 Common Issues & Solutions

### "Port 8000 already in use"
```bash
# Find process using port
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### "Flutter doctor shows issues"
```bash
# Accept Android licenses
flutter doctor --android-licenses

# Install iOS tools (macOS)
sudo gem install cocoapods
pod setup
```

### "Database connection failed"
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart database
docker-compose restart postgres

# Reset database (WARNING: destroys data)
docker-compose down -v
docker-compose up -d postgres
```

### "Build fails with Freezed errors"
```bash
# Clean generated files
flutter pub run build_runner clean

# Regenerate
flutter pub run build_runner build --delete-conflicting-outputs
```

### "Tests are failing"
```bash
# Backend: Run specific test
poetry run pytest app/tests/unit/test_specific.py -v

# Frontend: Run specific test
flutter test test/specific_test.dart

# Check test coverage
poetry run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 📞 Getting Help

### Communication Channels

- **Slack:** #rifa1122-dev for general discussion
- **GitHub Issues:** For bugs and feature requests
- **Pull Request Reviews:** Code review feedback
- **Documentation:** This guide and API docs

### When to Ask for Help

**Ask immediately if:**
- You're blocked for more than 30 minutes
- You need clarification on requirements
- You're unsure about architectural decisions
- You find a potential security issue

**Try to solve first:**
- Setup issues (check this guide)
- Simple bugs (use debugging tools)
- Code formatting issues (use linters)

### Code Review Process

**Reviewers will check:**
- ✅ Code follows style guidelines
- ✅ Tests are included and passing
- ✅ No security vulnerabilities
- ✅ Performance considerations
- ✅ Documentation updated
- ✅ Database migrations included (if needed)

**Common feedback areas:**
- Missing error handling
- Inefficient database queries
- Poor variable naming
- Missing tests
- Breaking API changes

---

## 🎓 Learning Resources

### Recommended Reading

**Backend:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://sqlalchemy.org/)
- [Pydantic Models](https://pydantic-docs.helpmanual.io/)
- [Celery Tasks](https://docs.celeryproject.org/)

**Frontend:**
- [Flutter Documentation](https://flutter.dev/docs)
- [Riverpod State Management](https://riverpod.dev/)
- [Freezed Code Generation](https://pub.dev/packages/freezed)

**General:**
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Testing Best Practices](https://martinfowler.com/bliki/TestPyramid.html)

### Online Courses

- [Flutter Development Course](https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/)
- [FastAPI Course](https://www.udemy.com/course/complete-fastapi/)
- [Docker for Developers](https://www.udemy.com/course/docker-for-developers/)

---

## 🚀 Next Steps

### Week 1: Getting Comfortable
- [ ] Complete setup and run both apps locally
- [ ] Explore the codebase and understand architecture
- [ ] Make a small change (e.g., update a UI string)
- [ ] Write and run tests for your change

### Week 2: First Contributions
- [ ] Pick an easy issue from the project board
- [ ] Implement the feature following the workflow
- [ ] Submit a pull request
- [ ] Participate in code review

### Week 3: Independent Development
- [ ] Take ownership of a feature
- [ ] Write comprehensive tests
- [ ] Update documentation
- [ ] Deploy to staging environment

### Ongoing: Best Practices
- [ ] Review pull requests from others
- [ ] Help onboard new team members
- [ ] Contribute to documentation improvements
- [ ] Suggest process improvements

---

## 📝 Checklist for New Features

**Before starting:**
- [ ] Issue created and assigned
- [ ] Requirements reviewed and clarified
- [ ] Design/architecture discussed with team

**During development:**
- [ ] Branch created with descriptive name
- [ ] Tests written (TDD preferred)
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Manual testing completed

**Before PR:**
- [ ] All tests passing
- [ ] Code reviewed by yourself
- [ ] No linting errors
- [ ] Commit messages are clear
- [ ] Breaking changes documented

**After merge:**
- [ ] Feature tested in staging
- [ ] Documentation deployed
- [ ] Team notified of new feature

---

Welcome aboard! We're excited to have you on the team. Remember: **done is better than perfect**. Don't hesitate to ask questions and contribute early and often! 🎯