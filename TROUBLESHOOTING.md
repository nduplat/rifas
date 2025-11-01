# Troubleshooting Guide

This guide provides solutions to common issues encountered while developing, testing, and deploying the Rifa1122 lottery system.

## Table of Contents

- [Development Environment Issues](#development-environment-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Database Issues](#database-issues)
- [API Issues](#api-issues)
- [Testing Issues](#testing-issues)
- [Deployment Issues](#deployment-issues)
- [Performance Issues](#performance-issues)
- [Security Issues](#security-issues)
- [Frequently Asked Questions](#frequently-asked-questions)

## Development Environment Issues

### Flutter Doctor Shows Issues

**Problem:** `flutter doctor` reports missing dependencies or configuration issues.

**Solutions:**

1. **Android SDK issues:**
   ```bash
   # Install Android SDK components
   flutter doctor --android-licenses

   # Or manually install via Android Studio SDK Manager
   ```

2. **iOS development on macOS:**
   ```bash
   # Install Xcode command line tools
   xcode-select --install

   # Install CocoaPods
   sudo gem install cocoapods
   pod setup
   ```

3. **Flutter SDK path issues:**
   ```bash
   # Add Flutter to PATH (in ~/.bashrc or ~/.zshrc)
   export PATH="$PATH:/path/to/flutter/bin"

   # Reload shell
   source ~/.bashrc
   ```

4. **VS Code extensions:**
   - Install Flutter and Dart extensions
   - Reload VS Code window

### Poetry/Python Environment Issues

**Problem:** Poetry installation or dependency issues.

**Solutions:**

1. **Poetry not found:**
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -

   # Add to PATH
   export PATH="$PATH:$HOME/.local/bin"
   ```

2. **Dependency conflicts:**
   ```bash
   # Clear Poetry cache
   poetry cache clear --all pypi

   # Remove poetry.lock and recreate
   rm poetry.lock
   poetry install
   ```

3. **Python version issues:**
   ```bash
   # Check Python version
   python3 --version

   # Use pyenv to manage Python versions
   pyenv install 3.11.0
   pyenv local 3.11.0
   ```

### Docker Issues

**Problem:** Docker containers fail to start or have connectivity issues.

**Solutions:**

1. **Port conflicts:**
   ```bash
   # Find process using port
   lsof -ti:8000 | xargs kill -9

   # Or change port in docker-compose.yml
   ports:
     - "8001:8000"
   ```

2. **Permission issues:**
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER

   # Restart session or run:
   newgrp docker
   ```

3. **Docker Compose issues:**
   ```bash
   # Stop all containers
   docker-compose down -v

   # Rebuild and start
   docker-compose up -d --build
   ```

## Backend Issues

### Application Won't Start

**Problem:** FastAPI application fails to start.

**Solutions:**

1. **Missing environment variables:**
   ```bash
   # Check .env file exists
   ls -la .env

   # Copy from example
   cp .env.example .env

   # Edit with proper values
   nano .env
   ```

2. **Database connection issues:**
   ```bash
   # Test database connection
   docker-compose exec postgres pg_isready -U rifa_user -d rifa1122

   # Check database logs
   docker-compose logs postgres
   ```

3. **Port already in use:**
   ```bash
   # Find and kill process
   lsof -ti:8000 | xargs kill -9
   ```

4. **Import errors:**
   ```bash
   # Check Python path
   cd backend
   python -c "import app.main"

   # Install missing dependencies
   poetry install
   ```

### Database Migration Issues

**Problem:** Alembic migrations fail.

**Solutions:**

1. **Migration conflicts:**
   ```bash
   # Check migration status
   poetry run alembic current

   # View migration history
   poetry run alembic history

   # Reset to clean state (WARNING: destroys data)
   poetry run alembic downgrade base
   poetry run alembic upgrade head
   ```

2. **Migration file issues:**
   ```bash
   # Edit migration manually
   nano alembic/versions/xxxxx_migration.py

   # Or recreate migration
   rm alembic/versions/xxxxx_migration.py
   poetry run alembic revision --autogenerate -m "fixed migration"
   ```

### Celery Worker Issues

**Problem:** Background tasks not executing.

**Solutions:**

1. **Workers not running:**
   ```bash
   # Check worker status
   docker-compose ps worker

   # View worker logs
   docker-compose logs worker

   # Restart workers
   docker-compose restart worker
   ```

2. **Redis connection issues:**
   ```bash
   # Test Redis connection
   docker-compose exec redis redis-cli ping

   # Check Redis logs
   docker-compose logs redis
   ```

3. **Task failures:**
   ```bash
   # Monitor tasks with Flower
   # Open http://localhost:5555

   # Check task status programmatically
   from app.core.celery_app import celery_app
   i = celery_app.control.inspect()
   print(i.active())
   ```

## Frontend Issues

### Build Failures

**Problem:** Flutter build fails.

**Solutions:**

1. **Clean build:**
   ```bash
   flutter clean
   flutter pub get
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

2. **iOS build issues:**
   ```bash
   cd ios
   pod install
   cd ..
   flutter build ios
   ```

3. **Android build issues:**
   ```bash
   flutter build apk --debug
   ```

4. **Web build issues:**
   ```bash
   flutter build web --release
   ```

### Hot Reload Not Working

**Problem:** Changes not reflecting in app during development.

**Solutions:**

1. **Restart development server:**
   ```bash
   # Stop current session (Ctrl+C)
   # Restart
   flutter run
   ```

2. **Clear cache:**
   ```bash
   flutter clean
   flutter pub get
   ```

3. **Check device connection:**
   ```bash
   flutter devices
   flutter run -d <device-id>
   ```

### State Management Issues

**Problem:** Riverpod providers not updating UI.

**Solutions:**

1. **Provider scope issues:**
   ```dart
   // Wrap app with ProviderScope
   void main() {
     runApp(
       const ProviderScope(
         child: MyApp(),
       ),
     );
   }
   ```

2. **Provider overrides in tests:**
   ```dart
   testWidgets('Test with mocked provider', (tester) async {
     await tester.pumpWidget(
       ProviderScope(
         overrides: [
           myProvider.overrideWithValue(mockValue),
         ],
         child: MyWidget(),
       ),
     );
   });
   ```

3. **Consumer widget issues:**
   ```dart
   // Use ConsumerWidget instead of StatelessWidget
   class MyWidget extends ConsumerWidget {
     @override
     Widget build(BuildContext context, WidgetRef ref) {
       final value = ref.watch(myProvider);
       return Text(value.toString());
     }
   }
   ```

## Database Issues

### Connection Pool Exhaustion

**Problem:** "Too many connections" database errors.

**Solutions:**

1. **Increase connection pool size:**
   ```python
   # In database configuration
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,      # Maximum connections
       max_overflow=30,   # Additional overflow connections
   )
   ```

2. **Check for connection leaks:**
   ```python
   # Ensure sessions are properly closed
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()  # Always close connections
   ```

3. **Monitor active connections:**
   ```sql
   -- Check active connections
   SELECT count(*) FROM pg_stat_activity WHERE datname = 'rifa1122';
   ```

### Data Corruption Issues

**Problem:** Inconsistent or corrupted data in database.

**Solutions:**

1. **Check database integrity:**
   ```sql
   -- Run vacuum analyze
   VACUUM ANALYZE;

   -- Check for corruption
   SELECT * FROM pg_stat_user_tables WHERE n_tup_ins = 0 AND n_tup_upd = 0;
   ```

2. **Restore from backup:**
   ```bash
   # Use backup script
   ./scripts/backup.sh

   # Restore from backup
   pg_restore -U rifa_user -d rifa1122 backup_file.dump
   ```

3. **Fix constraint violations:**
   ```sql
   -- Find orphaned records
   SELECT * FROM tickets WHERE rifa_id NOT IN (SELECT id FROM rifas);

   -- Clean up orphaned data
   DELETE FROM tickets WHERE rifa_id NOT IN (SELECT id FROM rifas);
   ```

### Slow Queries

**Problem:** Database queries are slow.

**Solutions:**

1. **Add database indexes:**
   ```sql
   -- Add index on frequently queried columns
   CREATE INDEX idx_tickets_rifa_id ON tickets(rifa_id);
   CREATE INDEX idx_tickets_usuario_id ON tickets(usuario_id);
   CREATE INDEX idx_rifas_estado ON rifas(estado);
   ```

2. **Analyze query performance:**
   ```sql
   -- Enable query logging
   ALTER DATABASE rifa1122 SET log_statement = 'all';
   ALTER DATABASE rifa1122 SET log_duration = on;

   -- View slow queries
   SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
   ```

3. **Optimize queries:**
   ```python
   # Use selectinload for relationships
   from sqlalchemy.orm import selectinload

   query = db.query(Rifa).options(
       selectinload(Rifa.categoria),
       selectinload(Rifa.loteria)
   ).filter(Rifa.estado == "activa")
   ```

## API Issues

### Authentication Problems

**Problem:** JWT tokens not working or expiring unexpectedly.

**Solutions:**

1. **Token format issues:**
   ```python
   # Check token structure
   import jwt
   decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
   print(decoded)
   ```

2. **Token expiration:**
   ```python
   # Check token expiry
   import jwt
   from datetime import datetime, timezone

   try:
       payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
       exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
       if exp < datetime.now(timezone.utc):
           print("Token expired")
   except jwt.ExpiredSignatureError:
       print("Token has expired")
   ```

3. **Invalid signature:**
   ```python
   # Verify SECRET_KEY matches between encoding/decoding
   print("SECRET_KEY length:", len(SECRET_KEY))
   ```

### Rate Limiting Issues

**Problem:** Requests being blocked by rate limiter.

**Solutions:**

1. **Check rate limit configuration:**
   ```python
   # In rate_limiting.py
   limiter = Limiter(key_func=get_remote_address)
   ```

2. **Override limits for testing:**
   ```python
   # Temporarily disable rate limiting
   limiter.enabled = False
   ```

3. **Check Redis storage:**
   ```bash
   # View rate limit keys in Redis
   docker-compose exec redis redis-cli KEYS "limiter:*"
   ```

### CORS Issues

**Problem:** Cross-origin requests blocked.

**Solutions:**

1. **Check CORS configuration:**
   ```python
   # In main.py
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000", "http://localhost:5000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Test CORS headers:**
   ```bash
   curl -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: GET" \
        -X OPTIONS \
        http://localhost:8000/api/v1/rifas/
   ```

## Testing Issues

### Tests Failing Intermittently

**Problem:** Tests pass sometimes but fail others (flaky tests).

**Solutions:**

1. **Time-dependent tests:**
   ```python
   # Use freezegun to mock time
   from freezegun import freeze_time

   @freeze_time("2024-01-01")
   def test_time_dependent_function():
       # Test code here
       pass
   ```

2. **Async test issues:**
   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       # Ensure proper async/await usage
       result = await my_async_function()
       assert result == expected
   ```

3. **Database state issues:**
   ```python
   # Use fixtures with proper cleanup
   @pytest.fixture(autouse=True)
   def clean_db(db_session):
       # Clean up before each test
       db_session.query(MyModel).delete()
       db_session.commit()
       yield
   ```

### Coverage Issues

**Problem:** Test coverage is low or inaccurate.

**Solutions:**

1. **Check coverage configuration:**
   ```ini
   # In pyproject.toml
   [tool.coverage.run]
   source = ["app"]
   omit = ["*/tests/*", "*/migrations/*"]

   [tool.coverage.report]
   exclude_lines = [
       "pragma: no cover",
       "def __repr__",
       "raise AssertionError",
       "raise NotImplementedError",
   ]
   ```

2. **Run coverage with source:**
   ```bash
   poetry run pytest --cov=app --cov-report=html --cov-report=term
   ```

3. **Debug missing coverage:**
   ```bash
   # Check which lines are not covered
   poetry run pytest --cov=app --cov-report=html
   # Open htmlcov/index.html
   ```

## Deployment Issues

### Container Startup Failures

**Problem:** Docker containers fail to start in production.

**Solutions:**

1. **Check environment variables:**
   ```bash
   # Verify .env file
   cat .env

   # Check container environment
   docker-compose exec api env | grep -E "(DATABASE|REDIS|SECRET)"
   ```

2. **Check logs:**
   ```bash
   docker-compose logs api
   docker-compose logs postgres
   docker-compose logs redis
   ```

3. **Health check failures:**
   ```bash
   # Test health endpoint manually
   curl http://localhost:8000/health

   # Check database connectivity
   docker-compose exec api python -c "
   from app.db.session import engine
   from sqlalchemy import text
   with engine.connect() as conn:
       result = conn.execute(text('SELECT 1'))
       print('DB connection OK')
   "
   ```

### SSL/TLS Issues

**Problem:** HTTPS not working or certificate errors.

**Solutions:**

1. **Certificate installation:**
   ```bash
   # Check certificate files
   ls -la /etc/nginx/ssl/

   # Test certificate
   openssl x509 -in /etc/nginx/ssl/cert.pem -text -noout
   ```

2. **Nginx configuration:**
   ```nginx
   server {
       listen 443 ssl http2;
       server_name your-domain.com;

       ssl_certificate /etc/nginx/ssl/cert.pem;
       ssl_certificate_key /etc/nginx/ssl/key.pem;

       # SSL security settings
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
       ssl_prefer_server_ciphers off;
   }
   ```

3. **Renew certificates:**
   ```bash
   # Using Certbot for Let's Encrypt
   certbot renew
   docker-compose restart nginx
   ```

### Load Balancing Issues

**Problem:** Requests not distributing properly across instances.

**Solutions:**

1. **Check load balancer configuration:**
   ```nginx
   upstream api_backend {
       least_conn;  # Use least connections algorithm
       server api1:8000;
       server api2:8000;
       server api3:8000;
   }
   ```

2. **Session stickiness:**
   ```nginx
   upstream api_backend {
       ip_hash;  # Sticky sessions based on IP
       server api1:8000;
       server api2:8000;
   }
   ```

3. **Health checks:**
   ```nginx
   server api1:8000;
   server api2:8000;

   # Only send requests to healthy servers
   check interval=3000 rise=2 fall=5 timeout=1000 type=http;
   check_http_send "GET /health HTTP/1.0\r\n\r\n";
   check_http_expect_alive http_2xx;
   ```

## Performance Issues

### Slow API Responses

**Problem:** API endpoints are slow.

**Solutions:**

1. **Database query optimization:**
   ```python
   # Use select only needed columns
   query = db.query(Rifa.id, Rifa.nombre).filter(Rifa.estado == "activa")

   # Use joins instead of N+1 queries
   query = db.query(Rifa).join(Rifa.categoria).options(contains_eager(Rifa.categoria))
   ```

2. **Add caching:**
   ```python
   from app.core.cache import cache

   @cache(expire=300)  # Cache for 5 minutes
   async def get_raffles():
       return db.query(Rifa).all()
   ```

3. **Profile performance:**
   ```python
   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()
   # Code to profile
   profiler.disable()

   stats = pstats.Stats(profiler).sort_stats('cumtime')
   stats.print_stats()
   ```

### Memory Leaks

**Problem:** Application memory usage keeps growing.

**Solutions:**

1. **Check for object leaks:**
   ```python
   # Use memory profiler
   from memory_profiler import profile

   @profile
   def my_function():
       # Code to profile
       pass
   ```

2. **Database connection leaks:**
   ```python
   # Ensure connections are closed
   @contextmanager
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```

3. **Cache memory issues:**
   ```python
   # Set cache limits
   cache_config = {
       'CACHE_TYPE': 'redis',
       'CACHE_REDIS_HOST': 'redis',
       'CACHE_REDIS_PORT': 6379,
       'CACHE_REDIS_DB': 1,
       'CACHE_DEFAULT_TIMEOUT': 300,
   }
   ```

### High CPU Usage

**Problem:** Application consuming too much CPU.

**Solutions:**

1. **Profile CPU usage:**
   ```python
   import cProfile

   cProfile.run('my_function()', 'profile_output.prof')

   # Analyze with snakeviz
   # pip install snakeviz
   # snakeviz profile_output.prof
   ```

2. **Optimize algorithms:**
   ```python
   # Use more efficient data structures
   # Avoid nested loops
   # Use list comprehensions instead of loops
   ```

3. **Async operations:**
   ```python
   # Use async/await for I/O operations
   async def fetch_lottery_results():
       async with httpx.AsyncClient() as client:
           response = await client.get(lottery_api_url)
           return response.json()
   ```

## Security Issues

### Authentication Bypass

**Problem:** Users can access protected resources without proper authentication.

**Solutions:**

1. **Check JWT validation:**
   ```python
   # Verify token validation
   from app.core.security import verify_token

   try:
       payload = verify_token(token)
       user_id = payload.get("user_id")
   except Exception as e:
       raise HTTPException(status_code=401, detail="Invalid token")
   ```

2. **Role-based access:**
   ```python
   # Check user roles
   def require_role(required_role: str):
       def decorator(func):
           @wraps(func)
           async def wrapper(*args, **kwargs):
               current_user = kwargs.get('current_user')
               if current_user.rol != required_role:
                   raise HTTPException(status_code=403, detail="Insufficient permissions")
               return await func(*args, **kwargs)
           return wrapper
       return decorator
   ```

### Data Exposure

**Problem:** Sensitive data being exposed in API responses.

**Solutions:**

1. **Remove sensitive fields:**
   ```python
   class UserResponse(BaseModel):
       id: str
       nombre: str
       email: str
       rol: str
       creado_en: datetime

       class Config:
           orm_mode = True
           # Exclude sensitive fields
           fields = {'hashed_password': {'exclude': True}}
   ```

2. **Input validation:**
   ```python
   from pydantic import validator

   class UserCreate(BaseModel):
       nombre: str
       email: EmailStr  # Validates email format
       password: str

       @validator('password')
       def password_strength(cls, v):
           if len(v) < 8:
               raise ValueError('Password must be at least 8 characters')
           return v
   ```

### SQL Injection

**Problem:** Potential SQL injection vulnerabilities.

**Solutions:**

1. **Use parameterized queries:**
   ```python
   # Good - parameterized
   user = db.query(User).filter(User.email == email).first()

   # Bad - string formatting
   # user = db.execute(f"SELECT * FROM users WHERE email = '{email}'")
   ```

2. **Input sanitization:**
   ```python
   from bleach import clean

   # Sanitize HTML input
   clean_input = clean(user_input, tags=[], strip=True)
   ```

## Frequently Asked Questions

### General Questions

**Q: How do I reset the development environment?**
```bash
# Stop all services
docker-compose down -v

# Remove all containers and volumes
docker system prune -a --volumes

# Rebuild from scratch
docker-compose up -d --build
```

**Q: How do I update dependencies?**
```bash
# Backend
cd backend
poetry update

# Frontend
cd rifa1122
flutter pub upgrade
```

**Q: How do I view application logs?**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# With timestamps
docker-compose logs -f --timestamps
```

### Development Questions

**Q: How do I debug the backend?**
```python
# Add debug prints
print(f"Debug: {variable}")

# Use debugger
import pdb; pdb.set_trace()

# Check logs
docker-compose logs api
```

**Q: How do I debug the frontend?**
```dart
// Add debug prints
print('Debug: $variable');

// Use debugger in VS Code
// Set breakpoints and run in debug mode
```

**Q: How do I add a new API endpoint?**
1. Create the endpoint function in the appropriate router
2. Add the route to the router
3. Update the API documentation
4. Add tests for the endpoint
5. Update any relevant frontend code

### Deployment Questions

**Q: How do I deploy to production?**
1. Build Docker images
2. Push to container registry
3. Update environment variables
4. Run database migrations
5. Deploy containers
6. Update load balancer
7. Run health checks

**Q: How do I rollback a deployment?**
```bash
# Stop current deployment
docker-compose down

# Start previous version
docker-compose -f docker-compose.previous.yml up -d

# Or rollback specific service
docker-compose up -d --scale api=0
docker-compose up -d --scale api=3 --image=previous-image
```

**Q: How do I monitor production?**
- Check application health endpoints
- Monitor logs with log aggregation
- Set up alerts for errors and performance issues
- Use APM tools for detailed monitoring
- Monitor database performance and connections

### Database Questions

**Q: How do I backup the database?**
```bash
# Use the backup script
./scripts/backup.sh

# Or manually
docker-compose exec postgres pg_dump -U rifa_user rifa1122 > backup.sql
```

**Q: How do I restore from backup?**
```bash
# Restore from dump
docker-compose exec -T postgres psql -U rifa_user rifa1122 < backup.sql
```

**Q: How do I run database migrations in production?**
```bash
# Backup first
./scripts/backup.sh

# Run migrations
docker-compose exec api poetry run alembic upgrade head

# Verify migration success
docker-compose logs api
```

This troubleshooting guide covers the most common issues you'll encounter. If you encounter an issue not covered here, please check the GitHub Issues or create a new issue with detailed information about the problem.