# Rifa1122 Backend API

A comprehensive lottery and raffle management system built with FastAPI, PostgreSQL, Redis, and Celery. This backend serves the Flutter mobile application and provides a robust API for managing raffles, tickets, users, and automated winner selection.

## 🏗️ Architecture Overview

The system consists of:
- **FastAPI**: High-performance web framework for building APIs
- **PostgreSQL**: Primary database for persistent data
- **Redis**: Caching and message broker for Celery
- **Celery**: Asynchronous task processing for winner selection and payouts
- **Stripe**: Payment processing integration
- **Docker**: Containerized deployment

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Poetry (for dependency management)

### Local Development Setup

1. **Clone the repository and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Run the initialization script:**
   ```bash
   chmod +x ../scripts/init_local.sh
   ../scripts/init_local.sh
   ```

4. **Start the development server:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Flower (Celery monitoring): http://localhost:5555
   - pgAdmin: http://localhost:5050

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (OAuth2)

### Raffles (Rifas)
- `GET /api/v1/rifas/` - List all raffles
- `POST /api/v1/rifas/` - Create new raffle (operator only)
- `GET /api/v1/rifas/{rifa_id}` - Get raffle details
- `PUT /api/v1/rifas/{rifa_id}` - Update raffle (operator only)
- `DELETE /api/v1/rifas/{rifa_id}` - Delete raffle (operator only)
- `POST /api/v1/rifas/{rifa_id}/close` - Close raffle and select winners (operator only)
- `POST /api/v1/rifas/{rifa_id}/recalculate` - Recalculate winners (operator only)

### Tickets
- `GET /api/v1/tickets/` - List user's tickets
- `POST /api/v1/tickets/purchase` - Purchase tickets

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://rifa_user:rifa_password@postgres:5432/rifa1122` |
| `REDIS_HOST` | Redis host | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `SECRET_KEY` | JWT secret key | (required) |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `STRIPE_SECRET_KEY` | Stripe secret key | (required for payments) |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | (required for payments) |
| `DEBUG` | Debug mode | `false` |
| `APP_NAME` | Application name | `Rifa1122 API` |
| `API_V1_PREFIX` | API version prefix | `/api/v1` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | Celery result backend | `redis://redis:6379/0` |

## 🗄️ Database Schema

### Core Tables

#### Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    telefono VARCHAR,
    hashed_password VARCHAR NOT NULL,
    rol VARCHAR DEFAULT 'jugador',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Lotteries
```sql
CREATE TABLE loterias (
    id UUID PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    descripcion TEXT,
    frecuencia VARCHAR,
    url_resultados VARCHAR
);
```

#### Raffle Categories
```sql
CREATE TABLE categoria_rifas (
    id UUID PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    color VARCHAR,
    valor_boleta INTEGER NOT NULL,
    total_recaudo INTEGER NOT NULL,
    rake DECIMAL(3,2) NOT NULL,
    fondo_premios INTEGER NOT NULL,
    premio_por_ganador INTEGER NOT NULL,
    comentario VARCHAR
);
```

#### Raffles
```sql
CREATE TABLE rifas (
    id UUID PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    categoria_id UUID REFERENCES categoria_rifas(id),
    loteria_id UUID REFERENCES loterias(id),
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    numero_ganadores INTEGER DEFAULT 1,
    estado VARCHAR DEFAULT 'activa',
    total_boletas INTEGER DEFAULT 0
);
```

#### Tickets
```sql
CREATE TABLE tickets (
    id UUID PRIMARY KEY,
    rifa_id UUID REFERENCES rifas(id),
    usuario_id UUID REFERENCES users(id),
    numero INTEGER NOT NULL,
    comprado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR DEFAULT 'vendido',
    transaccion_id UUID
);
```

#### Winners
```sql
CREATE TABLE ganadores (
    id UUID PRIMARY KEY,
    ticket_id UUID REFERENCES tickets(id),
    monto_ganado INTEGER NOT NULL,
    fecha_pago TIMESTAMP,
    referencia_pago VARCHAR
);
```

#### Transactions
```sql
CREATE TABLE transacciones (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    amount INTEGER NOT NULL,
    currency VARCHAR DEFAULT 'COP',
    provider VARCHAR,
    provider_ref VARCHAR,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Background Tasks

### Celery Workers

The system uses Celery for asynchronous processing:

1. **close_rifa**: Automatically closes expired raffles and determines winners based on lottery results
2. **process_payouts**: Processes payments to winners via Stripe
3. **reconcile_loteria**: Periodic reconciliation of lottery results

### Running Workers

```bash
# Using the provided script
../scripts/run_worker.sh

# Or manually
celery -A app.core.celery_app worker --loglevel=info --concurrency=4
```

## 🚀 Deployment

### Docker Production Deployment

1. **Build and deploy:**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

2. **Scale workers:**
   ```bash
   docker-compose up -d --scale worker=3
   ```

### Manual Deployment

1. **Install dependencies:**
   ```bash
   poetry install --only=main
   ```

2. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Start server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Start Celery workers:**
   ```bash
   celery -A app.core.celery_app worker --loglevel=info
   ```

## 🧪 Testing

### Running Tests

```bash
# Unit tests
pytest app/tests/unit/ -v

# Integration tests
pytest app/tests/integration/ -v

# End-to-end tests
pytest app/tests/e2e/ -v

# With coverage
pytest --cov=app --cov-report=html
```

### Test Structure

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test API endpoints and database interactions
- **E2E tests**: Test complete user flows (purchase to payout)

## 📊 Monitoring

### Health Checks

- API Health: `GET /api/v1/health`
- Database connectivity check included

### Logging

- Structured logging with `structlog`
- Configurable log levels
- JSON format for production

### Metrics

- Prometheus metrics endpoint: `/metrics`
- Request latency, error rates, database connections

## 🔒 Security

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (jugador, operador, admin)

### API Security
- Rate limiting with SlowAPI
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

### Data Protection
- Environment variable management
- No sensitive data in logs
- Secure password policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs and monitoring dashboards

## 🔄 Version History

- **v1.0.0**: Initial release with core raffle functionality
- Complete user authentication and authorization
- Ticket purchasing with Stripe integration
- Automated winner selection and payout processing
- Docker containerization and deployment scripts
