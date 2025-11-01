# Contributing to Rifa1122

Thank you for your interest in contributing to Rifa1122! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Community](#community)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites

- Python 3.11+
- Flutter 3.9.2+
- Docker and Docker Compose
- Git
- VS Code (recommended) with Flutter and Python extensions

### Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-org/rifa1122.git
   cd rifa1122
   ```

2. **Set up the development environment:**
   ```bash
   # Backend setup
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   chmod +x ../scripts/init_local.sh
   ../scripts/init_local.sh

   # Frontend setup
   cd ../rifa1122
   flutter pub get
   flutter pub run build_runner build
   ```

3. **Verify setup:**
   ```bash
   # Start services
   cd backend && docker-compose up -d

   # Run Flutter app
   cd ../rifa1122 && flutter run
   ```

## Development Workflow

### 1. Choose an Issue

- Check the [GitHub Issues](https://github.com/your-org/rifa1122/issues) for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b bugfix/issue-description

# Or for documentation
git checkout -b docs/update-readme
```

### 3. Development Process

#### Backend Development
```bash
cd backend

# Activate virtual environment
poetry shell

# Run tests before changes
poetry run pytest app/tests/unit/ -v

# Make your changes...

# Format code
poetry run black .
poetry run isort .

# Run tests after changes
poetry run pytest app/tests/unit/ -v
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

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication flow

- Implement JWT token generation
- Add login/register endpoints
- Update user model with password hashing
- Add comprehensive tests

Closes #123"
```

#### Commit Message Format

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add ticket purchase functionality
fix: resolve payment webhook timeout issue
docs: update API documentation for v1.2.0
test: add integration tests for user registration
```

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
# Fill out the PR template with:
# - Description of changes
# - Screenshots/videos for UI changes
# - Testing instructions
# - Breaking changes (if any)
```

## Coding Standards

### Python (Backend)

#### Code Style
- Follow [PEP 8](https://pep8.org/) style guide
- Use `black` for code formatting (line length: 88 characters)
- Use `isort` for import sorting
- Use `ruff` for linting

#### Type Hints
- All functions must have type hints
- Use `Optional` for nullable types
- Use `Union` for multiple possible types

```python
from typing import Optional, List
from pydantic import BaseModel

def get_user(user_id: str) -> Optional[User]:
    # Implementation
    pass

class UserCreate(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
```

#### Documentation
- Use Google-style docstrings
- Document all public functions and classes
- Include parameter descriptions and return types

```python
def create_rifa(rifa_data: RifaCreate, db: Session) -> Rifa:
    """Create a new raffle.

    Args:
        rifa_data: The raffle creation data
        db: Database session

    Returns:
        The created raffle instance

    Raises:
        ValueError: If the raffle data is invalid
    """
    # Implementation
    pass
```

#### Error Handling
- Use custom exceptions for business logic errors
- Log errors appropriately
- Don't expose sensitive information in error messages

### Dart (Frontend)

#### Code Style
- Follow the [Dart Style Guide](https://dart.dev/guides/language/effective-dart/style)
- Use `flutter format` for formatting
- Use `flutter analyze` for linting

#### State Management
- Use Riverpod for all state management
- Prefer immutable data models with Freezed
- Separate business logic from UI

#### Widget Structure
```dart
class RaffleListScreen extends ConsumerWidget {
  const RaffleListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rafflesAsync = ref.watch(rafflesProvider);

    return rafflesAsync.when(
      data: (raffles) => RaffleList(raffles: raffles),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => ErrorWidget(error),
    );
  }
}
```

#### Naming Conventions
- Classes: `PascalCase`
- Variables: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Files: `snake_case.dart`

## Testing

### Backend Testing

#### Unit Tests
```python
# app/tests/unit/test_user_service.py
import pytest
from app.services.user_service import UserService

class TestUserService:
    def test_create_user_success(self, db_session):
        service = UserService()
        user_data = UserCreate(
            nombre="Test User",
            email="test@example.com",
            password="password123"
        )

        user = service.create_user(user_data, db_session)

        assert user.nombre == "Test User"
        assert user.email == "test@example.com"

    def test_create_user_duplicate_email(self, db_session):
        # Test duplicate email handling
        pass
```

#### Integration Tests
```python
# app/tests/integration/test_auth_endpoints.py
def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nombre": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
```

#### Running Tests
```bash
# Unit tests
poetry run pytest app/tests/unit/ -v

# Integration tests
poetry run pytest app/tests/integration/ -v

# All tests with coverage
poetry run pytest --cov=app --cov-report=html
```

### Frontend Testing

#### Widget Tests
```dart
// test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:rifa1122/main.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame
    await tester.pumpWidget(const MyApp());

    // Verify that our counter starts at 0
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap the '+' icon and trigger a frame
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify that our counter has incremented
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}
```

#### Integration Tests
```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:rifa1122/main.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('end-to-end test', (WidgetTester tester) async {
    // Build the app
    await tester.pumpWidget(const MyApp());

    // Navigate to login screen
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();

    // Enter credentials
    await tester.enterText(find.byKey(const Key('email_field')), 'test@example.com');
    await tester.enterText(find.byKey(const Key('password_field')), 'password123');

    // Submit login
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pumpAndSettle();

    // Verify login success
    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

#### Running Tests
```bash
# Unit and widget tests
flutter test

# Integration tests
flutter test integration_test/
```

### Testing Best Practices

- **Test Coverage**: Aim for 80%+ coverage
- **Test Naming**: `test_[function_name]_[scenario]`
- **Arrange-Act-Assert**: Structure tests clearly
- **Mock External Dependencies**: Use fixtures for API calls
- **Test Edge Cases**: Invalid inputs, error conditions
- **Continuous Integration**: All tests must pass before merge

## Submitting Changes

### Pull Request Template

When creating a PR, fill out the template:

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots of UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] Breaking changes documented
- [ ] PR description is clear

## Related Issues
Closes #123, #124
```

### Branch Naming

- `feature/description-of-feature`
- `bugfix/description-of-bug`
- `hotfix/critical-fix`
- `docs/update-documentation`
- `refactor/code-improvement`

## Review Process

### Review Checklist

**Code Quality:**
- [ ] Code follows style guidelines
- [ ] No linting errors
- [ ] Functions are well-documented
- [ ] Variables are properly named
- [ ] No unused imports or code

**Functionality:**
- [ ] Requirements are met
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Security considerations addressed

**Testing:**
- [ ] Unit tests included
- [ ] Integration tests included
- [ ] Tests pass
- [ ] Test coverage adequate

**Documentation:**
- [ ] Code is documented
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Breaking changes documented

### Review Comments

**Be constructive and specific:**
```markdown
❌ Bad: "This code is bad"
✅ Good: "Consider using a more descriptive variable name here. Maybe `user_repository` instead of `repo`?"
```

**Suggest improvements:**
```markdown
💡 Instead of handling the error here, consider moving this to a service layer for better separation of concerns.
```

### Approval Process

1. **Automated Checks**: CI/CD pipeline must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: All tests must pass
4. **Documentation**: Updated as needed
5. **Merge**: Squash merge with descriptive commit message

## Documentation

### Types of Documentation

- **Code Documentation**: Docstrings, comments
- **API Documentation**: OpenAPI/Swagger specs
- **User Documentation**: README, guides
- **Architecture Documentation**: System design docs

### Documentation Standards

- Use Markdown for all documentation
- Keep documentation close to code
- Update documentation with code changes
- Use clear, concise language
- Include code examples where helpful

### Updating Documentation

When making changes that affect documentation:

1. Update relevant docs in the same PR
2. Test documentation for accuracy
3. Ensure links and references work
4. Update table of contents if needed

## Issue Reporting

### Bug Reports

**Use the bug report template:**

```markdown
## Bug Description
Clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 91]
- App Version: [e.g., 1.0.0]

## Additional Context
Any other information about the problem.
```

### Feature Requests

**Use the feature request template:**

```markdown
## Feature Summary
Brief description of the feature.

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other ways to solve this problem.

## Additional Context
Screenshots, mockups, or examples.
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Request Comments**: Code review discussions
- **Slack/Teams**: Real-time communication (if available)

### Getting Help

1. **Check existing documentation** first
2. **Search GitHub Issues** for similar problems
3. **Create a new issue** if needed
4. **Ask in discussions** for general questions

### Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Mention in release notes
- Attribution in documentation
- Community recognition posts

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to Rifa1122! Your contributions help make this project better for everyone. 🎉