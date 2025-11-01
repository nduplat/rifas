# Rifa1122 Deployment Guide

This guide covers deployment strategies for the Rifa1122 lottery system in various environments including development, staging, and production.

## Deployment Overview

The Rifa1122 system consists of:
- **Backend**: FastAPI application with PostgreSQL, Redis, and Celery
- **Frontend**: Flutter web application
- **Infrastructure**: Docker containers for all services

## Environment Variables

### Required Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://rifa_user:rifa_password@your-db-host:5432/rifa1122

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_DB=0

# JWT Authentication
SECRET_KEY=your-super-secret-jwt-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Payment Processing
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key

# Application Settings
DEBUG=false
APP_NAME=Rifa1122 API
API_V1_PREFIX=/api/v1
ENVIRONMENT=production

# Celery
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

## Docker Production Deployment

### 1. Production Docker Compose

Create a `docker-compose.prod.yml` file:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: rifa1122_postgres_prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: rifa1122
      POSTGRES_USER: rifa_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    networks:
      - rifa_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rifa_user -d rifa1122"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache/Broker
  redis:
    image: redis:7-alpine
    container_name: rifa1122_redis_prod
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_prod_data:/data
    ports:
      - "6379:6379"
    networks:
      - rifa_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI API Service
  api:
    image: rifa1122/backend:latest
    container_name: rifa1122_api_prod
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://rifa_user:${DB_PASSWORD}@postgres:5432/rifa1122
      - REDIS_HOST=redis
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    volumes:
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - rifa_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Celery Worker
  worker:
    image: rifa1122/backend:latest
    container_name: rifa1122_worker_prod
    restart: unless-stopped
    command: celery -A app.core.celery_app worker --loglevel=info --concurrency=4
    environment:
      - DATABASE_URL=postgresql://rifa_user:${DB_PASSWORD}@postgres:5432/rifa1122
      - REDIS_HOST=redis
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    volumes:
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
      - api
    networks:
      - rifa_network

  # Celery Beat (Scheduled Tasks)
  beat:
    image: rifa1122/backend:latest
    container_name: rifa1122_beat_prod
    restart: unless-stopped
    command: celery -A app.core.celery_app beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://rifa_user:${DB_PASSWORD}@postgres:5432/rifa1122
      - REDIS_HOST=redis
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    volumes:
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
      - api
    networks:
      - rifa_network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: rifa1122_nginx_prod
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - api
    networks:
      - rifa_network

volumes:
  postgres_prod_data:
  redis_prod_data:

networks:
  rifa_network:
    driver: bridge
```

### 2. Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    upstream api_backend {
        server api:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # API endpoints
        location /api/ {
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support for potential future features
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Static files (if serving Flutter web)
        location /web/ {
            alias /usr/share/nginx/html/web/;
            try_files $uri $uri/ /web/index.html;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Redirect to HTTPS (optional)
        # return 301 https://$server_name$request_uri;
    }

    # HTTPS server (if using SSL)
    # server {
    #     listen 443 ssl http2;
    #     server_name your-domain.com;
    #
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #
    #     # ... same configuration as HTTP server above
    # }
}
```

### 3. Build and Deploy

```bash
# Build the backend image
cd backend
docker build -t rifa1122/backend:latest .

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Cloud Deployment Options

### AWS Deployment

#### Option 1: ECS Fargate

1. **Create ECR repository:**
   ```bash
   aws ecr create-repository --repository-name rifa1122/backend
   ```

2. **Build and push image:**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

   # Tag and push
   docker tag rifa1122/backend:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/rifa1122/backend:latest
   docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/rifa1122/backend:latest
   ```

3. **Create ECS cluster and services** using AWS Console or CloudFormation.

#### Option 2: Elastic Beanstalk

1. **Create `.ebextensions` directory** with configuration files.

2. **Deploy using EB CLI:**
   ```bash
   eb init rifa1122-backend
   eb create production-env
   eb deploy
   ```

### Google Cloud Platform

#### Cloud Run (Serverless)

```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: rifa1122-backend
spec:
  template:
    spec:
      containers:
      - image: gcr.io/your-project/rifa1122/backend:latest
        env:
        - name: DATABASE_URL
          value: "postgresql://..."
        - name: REDIS_HOST
          value: "your-redis-host"
        ports:
        - containerPort: 8000
```

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/rifa1122/backend
gcloud run deploy --image gcr.io/your-project/rifa1122/backend --platform managed
```

### DigitalOcean App Platform

1. **Create app specification** (`app.yaml`):
   ```yaml
   name: rifa1122-backend
   services:
   - name: api
     source_dir: backend
     github:
       repo: your-username/rifa1122
       branch: main
     run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DATABASE_URL
       value: ${database.DATABASE_URL}
     - key: REDIS_HOST
       value: ${redis.REDIS_HOST}
   databases:
   - name: database
     engine: PG
     version: "15"
     size: basic
   ```

2. **Deploy:**
   ```bash
   doctl apps create --spec app.yaml
   ```

## Flutter Web Deployment

### Build for Web

```bash
cd rifa1122

# Build for production
flutter build web --release

# The build artifacts will be stored in the `build/web/` directory
```

### Serve with Nginx

Add to your nginx configuration:

```nginx
location /web/ {
    alias /path/to/rifa1122/build/web/;
    try_files $uri $uri/ /web/index.html;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Deploy to Firebase Hosting

1. **Install Firebase CLI:**
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize Firebase:**
   ```bash
   firebase init hosting
   ```

3. **Deploy:**
   ```bash
   firebase deploy --only hosting
   ```

### Deploy to Vercel/Netlify

1. **Build the web app**
2. **Upload `build/web` directory** to your hosting provider
3. **Configure redirects** for SPA routing

## Database Migration

### Production Database Setup

1. **Create production database:**
   ```sql
   CREATE DATABASE rifa1122;
   CREATE USER rifa_user WITH PASSWORD 'your-secure-password';
   GRANT ALL PRIVILEGES ON DATABASE rifa1122 TO rifa_user;
   ```

2. **Run migrations:**
   ```bash
   # Locally or in container
   alembic upgrade head
   ```

3. **Load initial data:**
   ```bash
   # Use the same script as in setup
   python scripts/load_initial_data.py
   ```

## Monitoring and Logging

### Application Monitoring

1. **Health Checks:**
   - GET `/api/v1/health` - Application health
   - GET `/metrics` - Prometheus metrics

2. **Logging:**
   - Structured logging with JSON format
   - Log aggregation with ELK stack or similar

3. **Error Tracking:**
   - Sentry integration for error monitoring
   - Configure `SENTRY_DSN` environment variable

### Infrastructure Monitoring

1. **Docker Monitoring:**
   ```bash
   # Check container health
   docker ps
   docker stats

   # View logs
   docker-compose logs -f api
   ```

2. **Database Monitoring:**
   - Monitor connection pools
   - Set up alerts for high CPU/memory usage

## Backup Strategy

### Database Backups

1. **Automated backups:**
   ```bash
   # Use the provided backup script
   ./scripts/backup.sh
   ```

2. **Schedule regular backups:**
   ```bash
   # Add to crontab
   0 2 * * * /path/to/backup.sh
   ```

### File Backups

1. **Log files**
2. **Upload directories** (if any)
3. **SSL certificates**

## Security Considerations

### SSL/TLS Configuration

1. **Obtain SSL certificate** (Let's Encrypt recommended)
2. **Configure Nginx** for HTTPS
3. **Redirect HTTP to HTTPS**

### Environment Security

1. **Never commit secrets** to version control
2. **Use strong passwords** for database and Redis
3. **Restrict database access** to application servers only
4. **Enable firewall rules**

### API Security

1. **Rate limiting** is configured
2. **CORS** properly configured
3. **Input validation** with Pydantic
4. **SQL injection prevention** with SQLAlchemy

## Scaling

### Horizontal Scaling

1. **API Service:**
   ```bash
   docker-compose up -d --scale api=3
   ```

2. **Worker Service:**
   ```bash
   docker-compose up -d --scale worker=5
   ```

### Database Scaling

1. **Read replicas** for read-heavy operations
2. **Connection pooling** with PgBouncer
3. **Database sharding** for very high scale

### Caching Strategy

1. **Redis** for session storage and caching
2. **CDN** for static assets
3. **Database query caching**

## Rollback Strategy

### Blue-Green Deployment

1. **Deploy new version** alongside current version
2. **Test new version** thoroughly
3. **Switch traffic** to new version
4. **Keep old version** as rollback option

### Database Rollbacks

1. **Schema migrations** are reversible
2. **Data migrations** require careful planning
3. **Backup before** any schema changes

## Performance Optimization

### Backend Optimization

1. **Database indexing** on frequently queried columns
2. **Query optimization** and N+1 query prevention
3. **Caching** with Redis
4. **Async operations** with Celery

### Frontend Optimization

1. **Code splitting** and lazy loading
2. **Asset optimization** and compression
3. **CDN** for static assets
4. **Service workers** for caching

## Maintenance

### Regular Tasks

1. **Update dependencies** monthly
2. **Security patches** as needed
3. **Database maintenance** (vacuum, reindex)
4. **Log rotation** and cleanup

### Monitoring Alerts

1. **High error rates**
2. **Database connection issues**
3. **High memory/CPU usage**
4. **Payment processing failures**

## Troubleshooting Production Issues

### Common Issues

1. **Database connection timeouts:**
   - Check connection pool settings
   - Verify database server resources

2. **High latency:**
   - Check database query performance
   - Monitor Redis cache hit rates

3. **Payment failures:**
   - Verify Stripe webhook configuration
   - Check Stripe API key validity

4. **Container crashes:**
   - Check application logs
   - Verify environment variables
   - Monitor resource usage

### Debug Commands

```bash
# Check container status
docker-compose ps

# View application logs
docker-compose logs api

# Check database connections
docker-compose exec postgres pg_stat_activity;

# Test API endpoints
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/rifas/
```

## Cost Optimization

### Cloud Costs

1. **Right-size instances** based on load
2. **Use reserved instances** for predictable workloads
3. **Implement auto-scaling** to handle traffic spikes
4. **Choose appropriate storage** classes

### Database Costs

1. **Optimize queries** to reduce compute time
2. **Archive old data** to cheaper storage
3. **Use database replicas** for read operations

This deployment guide provides a comprehensive foundation for deploying Rifa1122 in production. Adjust configurations based on your specific requirements and infrastructure preferences.