# Testing Guide for Rifa1122

This document provides comprehensive guidelines for testing the Rifa1122 lottery system, including unit tests, integration tests, end-to-end tests, and testing best practices.

## Table of Contents

- [Testing Overview](#testing-overview)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [End-to-End Testing](#end-to-end-testing)
- [Test Data Management](#test-data-management)
- [Continuous Integration](#continuous-integration)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)
- [Testing Best Practices](#testing-best-practices)
- [Troubleshooting Tests](#troubleshooting-tests)

## Testing Overview

### Testing Pyramid

```
End-to-End Tests (E2E)
        ▲
        │  Fewer, slower, more comprehensive
        │
Integration Tests
        ▲
        │  Medium coverage, medium speed
        │
   Unit Tests
        │  Many, fast, focused
        ▼
```

### Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Key user flows
- **E2E Tests**: Critical user journeys
- **Performance Tests**: Load and stress testing

### Testing Tools

**Backend:**
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **httpx**: HTTP client for testing

**Frontend:**
- **flutter_test**: Flutter testing framework
- **mockito**: Mocking for Dart
- **integration_test**: E2E testing

## Backend Testing

### Project Structure

```
backend/app/tests/
├── unit/                    # Unit tests
│   ├── test_auth.py        # Authentication tests
│   ├── test_rifas.py       # Raffle tests
│   ├── test_tickets.py     # Ticket tests
│   └── test_services.py    # Service layer tests
├── integration/            # Integration tests
│   ├── test_auth_endpoints.py
│   ├── test_rifas_endpoints.py
│   └── test_purchase_flow.py
├── e2e/                    # End-to-end tests
│   └── test_purchase_flow.py
└── conftest.py             # Test configuration
```

### Unit Testing

#### Setting Up Unit Tests

```python
# app/tests/unit/test_user_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.user_service import UserService
from app.schemas.user import UserCreate

class TestUserService:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user_service = UserService()

    def test_create_user_success(self):
        """Test successful user creation."""
        user_data = UserCreate(
            nombre="Test User",
            email="test@example.com",
            password="securepassword123",
            rol="jugador"
        )

        # Mock the database session
        mock_db = Mock()
        mock_user = Mock()
        mock_user.id = "test-id"
        mock_user.nombre = user_data.nombre
        mock_user.email = user_data.email
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch('app.services.user_service.get_password_hash') as mock_hash:
            mock_hash.return_value = "hashed_password"
            with patch('app.models.user.User', return_value=mock_user):
                result = self.user_service.create_user(user_data, mock_db)

                assert result.nombre == "Test User"
                assert result.email == "test@example.com"
                mock_db.add.assert_called_once()
                mock_db.commit.assert_called_once()

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        user_data = UserCreate(
            nombre="Test User",
            email="existing@example.com",
            password="securepassword123"
        )

        mock_db = Mock()
        # Simulate database constraint violation
        mock_db.commit.side_effect = Exception("Unique constraint violated")

        with pytest.raises(Exception):
            self.user_service.create_user(user_data, mock_db)
```

#### Testing Database Operations

```python
# app/tests/unit/test_rifa_repository.py
import pytest
from app.repositories.rifa_repository import RifaRepository
from app.models.rifa import Rifa

class TestRifaRepository:
    def test_get_rifa_by_id_found(self, db_session):
        """Test retrieving a raffle by ID when it exists."""
        # Create test data
        rifa = Rifa(
            id="test-rifa-id",
            nombre="Test Raffle",
            categoria_id="test-category",
            loteria_id="test-lottery",
            fecha_inicio="2024-01-01T00:00:00Z",
            fecha_fin="2024-01-31T23:59:59Z",
            estado="activa"
        )
        db_session.add(rifa)
        db_session.commit()

        repository = RifaRepository()
        result = repository.get_by_id("test-rifa-id", db_session)

        assert result is not None
        assert result.id == "test-rifa-id"
        assert result.nombre == "Test Raffle"

    def test_get_rifa_by_id_not_found(self, db_session):
        """Test retrieving a raffle by ID when it doesn't exist."""
        repository = RifaRepository()
        result = repository.get_by_id("nonexistent-id", db_session)

        assert result is None
```

#### Testing API Endpoints

```python
# app/tests/unit/test_auth_endpoints.py
import pytest
from httpx import AsyncClient
from app.main import app

class TestAuthEndpoints:
    @pytest.mark.asyncio
    async def test_register_user_success(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "nombre": "Test User",
            "email": "test@example.com",
            "password": "securepassword123",
            "telefono": "+57 301 234 5678",
            "rol": "jugador"
        }

        response = await client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"
        assert data["nombre"] == "Test User"
        assert "hashed_password" not in data  # Password should not be returned

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, client: AsyncClient):
        """Test registration with duplicate email."""
        user_data = {
            "nombre": "Test User",
            "email": "duplicate@example.com",
            "password": "securepassword123"
        }

        # First registration
        response1 = await client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201

        # Duplicate registration
        response2 = await client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]
```

### Integration Testing

#### Testing Complete User Flows

```python
# app/tests/integration/test_purchase_flow.py
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

class TestPurchaseFlow:
    @pytest.mark.asyncio
    async def test_complete_ticket_purchase_flow(
        self, client: AsyncClient, db_session: Session, test_user_token: str
    ):
        """Test the complete ticket purchase flow from start to finish."""

        # 1. Create a raffle
        rifa_data = {
            "nombre": "Integration Test Raffle",
            "categoria_id": "550e8400-e29b-41d4-a716-446655440002",  # Bronze
            "loteria_id": "550e8400-e29b-41d4-a716-446655440001",   # Baloto
            "fecha_inicio": "2024-01-01T00:00:00Z",
            "fecha_fin": "2024-12-31T23:59:59Z",
            "numero_ganadores": 2
        }

        response = await client.post(
            "/api/v1/rifas/",
            json=rifa_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 201
        rifa_id = response.json()["id"]

        # 2. Purchase tickets
        purchase_data = {
            "rifa_id": rifa_id,
            "quantity": 3,
            "idempotency_key": "test-purchase-123"
        }

        response = await client.post(
            "/api/v1/tickets/purchase",
            json=purchase_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 201

        data = response.json()
        assert "tickets" in data
        assert len(data["tickets"]) == 3
        assert "transaccion_id" in data

        # 3. Verify tickets were created in database
        tickets_response = await client.get(
            "/api/v1/tickets/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert tickets_response.status_code == 200
        tickets = tickets_response.json()

        # Should have 3 tickets for this user
        rifa_tickets = [t for t in tickets if t["rifa_id"] == rifa_id]
        assert len(rifa_tickets) == 3

        # 4. Verify ticket numbers are unique
        ticket_numbers = [t["numero"] for t in rifa_tickets]
        assert len(set(ticket_numbers)) == 3  # All unique
```

#### Testing External API Integrations

```python
# app/tests/integration/test_stripe_webhooks.py
import pytest
from unittest.mock import patch
from httpx import AsyncClient
import json

class TestStripeWebhooks:
    @pytest.mark.asyncio
    async def test_stripe_payment_succeeded_webhook(self, client: AsyncClient):
        """Test handling of successful payment webhooks from Stripe."""

        webhook_payload = {
            "id": "evt_test_webhook",
            "object": "event",
            "api_version": "2020-08-27",
            "created": 1234567890,
            "data": {
                "object": {
                    "id": "pi_test_payment_intent",
                    "object": "payment_intent",
                    "amount": 15000,
                    "currency": "cop",
                    "status": "succeeded",
                    "metadata": {
                        "user_id": "test-user-id",
                        "rifa_id": "test-rifa-id"
                    }
                }
            },
            "type": "payment_intent.succeeded"
        }

        # Generate webhook signature (simplified for testing)
        signature = "t=1234567890,v1=test_signature"

        with patch('app.services.stripe_service.StripeService.verify_webhook_signature') as mock_verify:
            mock_verify.return_value = True

            response = await client.post(
                "/api/v1/webhooks/stripe",
                json=webhook_payload,
                headers={
                    "Content-Type": "application/json",
                    "Stripe-Signature": signature
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Webhook processed successfully"
```

### Running Backend Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest app/tests/unit/test_auth.py

# Run specific test method
poetry run pytest app/tests/unit/test_auth.py::TestAuthEndpoints::test_register_user_success -v

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run integration tests only
poetry run pytest app/tests/integration/

# Run tests in parallel
poetry run pytest -n auto

# Run tests with detailed output
poetry run pytest -v -s
```

## Frontend Testing

### Widget Testing

```dart
// test/widget/login_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:rifa1122/features/auth/presentation/login_screen.dart';
import 'package:rifa1122/features/auth/data/auth_repository.dart';
import 'package:mockito/mockito.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late MockAuthRepository mockAuthRepository;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
  });

  testWidgets('Login screen shows email and password fields',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          authRepositoryProvider.overrideWithValue(mockAuthRepository),
        ],
        child: const MaterialApp(home: LoginScreen()),
      ),
    );

    // Verify email field is present
    expect(find.byKey(const Key('email_field')), findsOneWidget);

    // Verify password field is present
    expect(find.byKey(const Key('password_field')), findsOneWidget);

    // Verify login button is present
    expect(find.byKey(const Key('login_button')), findsOneWidget);
  });

  testWidgets('Login button triggers authentication',
      (WidgetTester tester) async {
    when(mockAuthRepository.login(any, any))
        .thenAnswer((_) async => 'mock_token');

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          authRepositoryProvider.overrideWithValue(mockAuthRepository),
        ],
        child: const MaterialApp(home: LoginScreen()),
      ),
    );

    // Enter email
    await tester.enterText(
        find.byKey(const Key('email_field')), 'test@example.com');

    // Enter password
    await tester.enterText(
        find.byKey(const Key('password_field')), 'password123');

    // Tap login button
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pump();

    // Verify login was called
    verify(mockAuthRepository.login('test@example.com', 'password123'))
        .called(1);
  });
}
```

### Provider Testing

```dart
// test/provider/auth_provider_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:rifa1122/features/auth/data/auth_repository.dart';
import 'package:rifa1122/features/auth/presentation/auth_provider.dart';
import 'package:mockito/mockito.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late MockAuthRepository mockAuthRepository;
  late ProviderContainer container;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
    container = ProviderContainer(
      overrides: [
        authRepositoryProvider.overrideWithValue(mockAuthRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  test('Login provider updates state on successful login', () async {
    when(mockAuthRepository.login('test@example.com', 'password123'))
        .thenAnswer((_) async => 'mock_jwt_token');

    final loginNotifier = container.read(loginProvider.notifier);

    // Initial state should be idle
    expect(container.read(loginProvider), const AsyncValue.data(null));

    // Perform login
    await loginNotifier.login('test@example.com', 'password123');

    // Verify state updated
    final state = container.read(loginProvider);
    expect(state.value, 'mock_jwt_token');

    // Verify repository was called
    verify(mockAuthRepository.login('test@example.com', 'password123'))
        .called(1);
  });

  test('Login provider handles errors correctly', () async {
    when(mockAuthRepository.login(any, any))
        .thenThrow(Exception('Invalid credentials'));

    final loginNotifier = container.read(loginProvider.notifier);

    await loginNotifier.login('wrong@email.com', 'wrongpassword');

    final state = container.read(loginProvider);
    expect(state.hasError, true);
    expect(state.error, isA<Exception>());
  });
}
```

### Integration Testing

```dart
// integration_test/login_flow_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:rifa1122/main.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Complete login flow', (WidgetTester tester) async {
    // Build the app
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    // Navigate to login screen (assuming there's a login button on home)
    await tester.tap(find.byKey(const Key('go_to_login_button')));
    await tester.pumpAndSettle();

    // Verify we're on the login screen
    expect(find.byKey(const Key('login_screen')), findsOneWidget);

    // Enter valid credentials
    await tester.enterText(
        find.byKey(const Key('email_field')), 'test@example.com');
    await tester.enterText(
        find.byKey(const Key('password_field')), 'password123');

    // Submit login
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();

    // Verify successful login - should navigate to home screen
    expect(find.byKey(const Key('home_screen')), findsOneWidget);
    expect(find.text('Welcome'), findsOneWidget);
  });

  testWidgets('Login with invalid credentials shows error',
      (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    // Navigate to login
    await tester.tap(find.byKey(const Key('go_to_login_button')));
    await tester.pumpAndSettle();

    // Enter invalid credentials
    await tester.enterText(
        find.byKey(const Key('email_field')), 'invalid@email.com');
    await tester.enterText(
        find.byKey(const Key('password_field')), 'wrongpassword');

    // Submit login
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();

    // Verify error message is shown
    expect(find.text('Invalid credentials'), findsOneWidget);
    expect(find.byKey(const Key('home_screen')), findsNothing);
  });
}
```

### Running Frontend Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget/login_screen_test.dart

# Run with coverage
flutter test --coverage

# Run integration tests
flutter test integration_test/

# Run tests on specific device
flutter test --device-id=<device-id>
```

## End-to-End Testing

### Complete User Journey Testing

```python
# app/tests/e2e/test_complete_user_journey.py
import pytest
from playwright.sync_api import Page, expect
from app.tests.e2e.conftest import TestApp

class TestCompleteUserJourney:
    def test_user_registers_purchases_ticket_and_wins(self, test_app: TestApp, page: Page):
        """Test complete user journey from registration to winning a raffle."""

        # 1. User visits the app
        page.goto(test_app.url)

        # 2. User registers
        page.click("text=Register")
        page.fill("[data-testid=email]", "test@example.com")
        page.fill("[data-testid=password]", "password123")
        page.fill("[data-testid=name]", "Test User")
        page.click("[data-testid=register-button]")

        # Verify registration success
        expect(page.locator("text=Welcome, Test User")).to_be_visible()

        # 3. User browses raffles
        page.click("text=Raffles")
        expect(page.locator("text=Available Raffles")).to_be_visible()

        # 4. User selects a raffle
        page.click("[data-testid=raffle-card]:first-child")
        expect(page.locator("[data-testid=raffle-details]")).to_be_visible()

        # 5. User purchases tickets
        page.fill("[data-testid=quantity]", "3")
        page.click("[data-testid=purchase-button]")

        # Handle Stripe payment (mocked in test environment)
        page.click("[data-testid=confirm-payment]")

        # Verify purchase success
        expect(page.locator("text=Purchase successful!")).to_be_visible()
        expect(page.locator("text=Your tickets:")).to_be_visible()

        # 6. User views their tickets
        page.click("text=My Tickets")
        expect(page.locator("[data-testid=ticket-list]")).to_be_visible()
        expect(page.locator("[data-testid=ticket-item]")).to_have_count(3)

        # 7. Raffle closes and winner is selected (simulated)
        # This would be triggered by a background job in production
        test_app.trigger_winner_selection(raffle_id)

        # 8. User checks if they won
        page.reload()
        page.click("text=My Tickets")

        # Check if winner notification appears
        winner_notification = page.locator("[data-testid=winner-notification]")
        if winner_notification.is_visible():
            expect(winner_notification).to_contain_text("Congratulations!")
        else:
            expect(page.locator("text=Better luck next time")).to_be_visible()
```

### API Testing with Real Database

```python
# app/tests/e2e/test_api_endpoints.py
import pytest
from httpx import AsyncClient
import asyncio

class TestAPIEndpointsE2E:
    @pytest.mark.asyncio
    async def test_full_raffle_lifecycle(self, client: AsyncClient, db_session):
        """Test complete raffle lifecycle through API."""

        # 1. Create user
        user_data = {
            "nombre": "E2E Test User",
            "email": "e2e@example.com",
            "password": "testpassword123"
        }
        user_response = await client.post("/api/v1/auth/register", json=user_data)
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        # 2. Login to get token
        login_data = {
            "username": "e2e@example.com",
            "password": "testpassword123"
        }
        login_response = await client.post("/api/v1/auth/login", data=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Set authorization header for subsequent requests
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create raffle (admin/operador only - would need different token)
        # This step might be skipped or use a different user

        # 4. List available raffles
        raffles_response = await client.get("/api/v1/rifas/", headers=headers)
        assert raffles_response.status_code == 200
        raffles = raffles_response.json()
        assert isinstance(raffles, list)

        if raffles:  # If there are raffles available
            rifa_id = raffles[0]["id"]

            # 5. Get raffle details
            detail_response = await client.get(f"/api/v1/rifas/{rifa_id}", headers=headers)
            assert detail_response.status_code == 200

            # 6. Purchase tickets
            purchase_data = {
                "rifa_id": rifa_id,
                "quantity": 2,
                "idempotency_key": "e2e-test-purchase-123"
            }
            purchase_response = await client.post(
                "/api/v1/tickets/purchase",
                json=purchase_data,
                headers=headers
            )
            assert purchase_response.status_code == 201

            # 7. Verify tickets were created
            tickets_response = await client.get("/api/v1/tickets/", headers=headers)
            assert tickets_response.status_code == 200
            tickets = tickets_response.json()

            # Filter tickets for this raffle
            rifa_tickets = [t for t in tickets if t["rifa_id"] == rifa_id]
            assert len(rifa_tickets) == 2
```

## Test Data Management

### Fixtures and Test Data

```python
# app/tests/conftest.py
import pytest
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.models import *

@pytest.fixture(scope="session")
def db_session():
    """Create a test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield session

    # Clean up
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        id="test-user-id",
        nombre="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        rol="jugador"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_raffle(db_session):
    """Create a test raffle."""
    raffle = Rifa(
        id="test-raffle-id",
        nombre="Test Raffle",
        categoria_id="test-category-id",
        loteria_id="test-lottery-id",
        fecha_inicio="2024-01-01T00:00:00Z",
        fecha_fin="2024-12-31T23:59:59Z",
        estado="activa"
    )
    db_session.add(raffle)
    db_session.commit()
    return raffle

@pytest.fixture
async def client():
    """Create an async test client."""
    from httpx import AsyncClient
    from app.main import app

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
```

### Mock Data for External Services

```python
# app/tests/mocks/stripe_mock.py
import json
from unittest.mock import Mock

def mock_stripe_payment_intent():
    """Mock Stripe PaymentIntent object."""
    payment_intent = Mock()
    payment_intent.id = "pi_mock_payment_intent"
    payment_intent.amount = 15000
    payment_intent.currency = "cop"
    payment_intent.status = "succeeded"
    payment_intent.metadata = {
        "user_id": "test-user-id",
        "rifa_id": "test-raffle-id"
    }
    return payment_intent

def mock_stripe_webhook_payload():
    """Mock Stripe webhook payload."""
    return {
        "id": "evt_mock_webhook",
        "object": "event",
        "type": "payment_intent.succeeded",
        "data": {
            "object": mock_stripe_payment_intent()
        }
    }
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -

    - name: Install dependencies
      run: poetry install

    - name: Run linting
      run: |
        poetry run black --check .
        poetry run isort --check-only .
        poetry run ruff check .

    - name: Run tests
      run: poetry run pytest --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_HOST: localhost

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.9.2'

    - name: Install dependencies
      run: flutter pub get

    - name: Run Flutter tests
      run: flutter test --coverage

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install Playwright
      run: npm ci

    - name: Run E2E tests
      run: npx playwright test
```

## Performance Testing

### Load Testing with Locust

```python
# performance_tests/locustfile.py
from locust import HttpUser, task, between
import json

class RaffleUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login and get token on start."""
        response = self.client.post("/api/v1/auth/login", data={
            "username": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def view_raffles(self):
        """View available raffles."""
        self.client.get("/api/v1/rifas/", headers=self.headers)

    @task(2)
    def view_raffle_details(self):
        """View specific raffle details."""
        # Assuming we have some raffle IDs
        raffle_ids = ["raffle-1", "raffle-2", "raffle-3"]
        raffle_id = random.choice(raffle_ids)
        self.client.get(f"/api/v1/rifas/{raffle_id}", headers=self.headers)

    @task(1)
    def purchase_tickets(self):
        """Purchase tickets (rate limited, so lower frequency)."""
        purchase_data = {
            "rifa_id": "raffle-1",
            "quantity": 1,
            "idempotency_key": f"perf-test-{self.user_id}-{time.time()}"
        }
        self.client.post(
            "/api/v1/tickets/purchase",
            json=purchase_data,
            headers=self.headers
        )
```

### Running Performance Tests

```bash
# Install Locust
pip install locust

# Run performance tests
locust -f performance_tests/locustfile.py --host http://localhost:8000

# Open web interface at http://localhost:8089
# Configure number of users and spawn rate
```

## Security Testing

### Authentication Testing

```python
# app/tests/security/test_auth_security.py
import pytest
from httpx import AsyncClient

class TestAuthenticationSecurity:
    @pytest.mark.asyncio
    async def test_brute_force_protection(self, client: AsyncClient):
        """Test that brute force attacks are prevented."""
        # Attempt multiple failed logins
        for i in range(10):
            response = await client.post("/api/v1/auth/login", data={
                "username": "test@example.com",
                "password": "wrongpassword"
            })

        # Should eventually be rate limited
        response = await client.post("/api/v1/auth/login", data={
            "username": "test@example.com",
            "password": "wrongpassword"
        })

        # Should return 429 Too Many Requests
        assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_jwt_token_expiry(self, client: AsyncClient):
        """Test that expired JWT tokens are rejected."""
        # This would require mocking time or using a short-lived token
        pass

    @pytest.mark.asyncio
    async def test_password_complexity(self, client: AsyncClient):
        """Test password complexity requirements."""
        weak_passwords = ["123", "password", "qwerty"]

        for password in weak_passwords:
            response = await client.post("/api/v1/auth/register", json={
                "nombre": "Test User",
                "email": f"test{password}@example.com",
                "password": password
            })

            # Should reject weak passwords
            assert response.status_code == 422  # Validation error
```

### API Security Testing

```python
# app/tests/security/test_api_security.py
import pytest
from httpx import AsyncClient

class TestAPISecurity:
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self, client: AsyncClient):
        """Test that SQL injection attacks are prevented."""
        malicious_input = "'; DROP TABLE users; --"

        response = await client.post("/api/v1/auth/register", json={
            "nombre": malicious_input,
            "email": "test@example.com",
            "password": "password123"
        })

        # Should not execute SQL injection
        assert response.status_code in [201, 400]  # Success or validation error
        # Table should still exist (would need separate verification)

    @pytest.mark.asyncio
    async def test_xss_prevention(self, client: AsyncClient):
        """Test that XSS attacks are prevented."""
        xss_payload = "<script>alert('XSS')</script>"

        response = await client.post("/api/v1/auth/register", json={
            "nombre": xss_payload,
            "email": "test@example.com",
            "password": "password123"
        })

        assert response.status_code == 201
        user_data = response.json()

        # XSS payload should be escaped or sanitized
        assert "<script>" not in user_data["nombre"]

    @pytest.mark.asyncio
    async def test_cors_policy(self, client: AsyncClient):
        """Test CORS policy is properly configured."""
        response = await client.options("/api/v1/rifas/",
            headers={
                "Origin": "https://malicious-site.com",
                "Access-Control-Request-Method": "GET"
            }
        )

        # Should not allow requests from unauthorized origins
        assert "Access-Control-Allow-Origin" not in response.headers or \
               response.headers["Access-Control-Allow-Origin"] != "https://malicious-site.com"
```

## Testing Best Practices

### Test Organization

1. **Arrange-Act-Assert (AAA)** pattern for all tests
2. **Descriptive test names** that explain what they're testing
3. **One assertion per test** when possible
4. **Test independence** - no shared state between tests
5. **Fast execution** - keep tests running quickly

### Code Coverage

- **Aim for 80%+ coverage** on critical business logic
- **Focus on branches and conditions**, not just lines
- **Don't test generated code** (e.g., Pydantic models, Freezed classes)
- **Use coverage reports** to identify untested code

### Mocking Strategy

- **Mock external dependencies** (Stripe, lottery APIs)
- **Don't mock your own code** - test real implementations
- **Use fixtures** for common test data
- **Verify interactions** with mocks when necessary

### Test Data Management

- **Use factories** for creating test data
- **Clean up after tests** to avoid interference
- **Use realistic data** that matches production
- **Version test data** with application changes

### Continuous Testing

- **Run tests on every commit** with CI/CD
- **Fail fast** - stop on first failure in CI
- **Parallel execution** to speed up test runs
- **Regular maintenance** of flaky tests

## Troubleshooting Tests

### Common Issues

**Tests are slow:**
- Mock external API calls
- Use in-memory databases for unit tests
- Run tests in parallel
- Profile slow tests with `--durations` flag

**Flaky tests:**
- Avoid time-dependent logic
- Use proper waits in async tests
- Ensure test isolation
- Fix race conditions

**False positives/negatives:**
- Review test assertions
- Check test setup and teardown
- Verify mock behavior
- Debug with print statements or debugger

**Database issues:**
- Use transactions that rollback
- Clean up test data properly
- Avoid shared database state
- Use unique identifiers for test data

### Debugging Tests

```bash
# Run specific test with verbose output
poetry run pytest app/tests/unit/test_auth.py::TestAuthEndpoints::test_register_user_success -v -s

# Run with debugging
poetry run pytest --pdb app/tests/unit/test_auth.py::TestAuthEndpoints::test_register_user_success

# Show durations of slowest tests
poetry run pytest --durations=10

# Run tests with coverage details
poetry run pytest --cov=app --cov-report=html && open htmlcov/index.html
```

### Test Maintenance

- **Regular review** of test suite health
- **Remove obsolete tests** when code changes
- **Update tests** when requirements change
- **Refactor tests** to improve readability
- **Document complex test scenarios**

This comprehensive testing guide provides the foundation for maintaining high-quality code in the Rifa1122 project. Regular testing ensures reliability, prevents regressions, and supports confident deployments.