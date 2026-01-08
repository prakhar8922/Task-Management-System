# Deployment Guide

This guide provides comprehensive instructions for deploying the Task Management System to various environments, from local development to production.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Static Files & Media](#static-files--media)
7. [Security Considerations](#security-considerations)
8. [Monitoring & Logging](#monitoring--logging)
9. [Troubleshooting](#troubleshooting)

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git
- PostgreSQL (optional, SQLite works for development)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd task_manager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### Step 2: Environment Configuration

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
# DATABASE_URL=sqlite:///db.sqlite3

# Or PostgreSQL for development
# DATABASE_URL=postgresql://username:password@localhost:5432/task_manager_dev

# CORS Settings (for React frontend)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata fixtures/initial_data.json
```

### Step 4: Start Development Servers

**Terminal 1 - Backend:**
```bash
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000/api/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🐳 Docker Deployment

### Development with Docker Compose

1. **Build and start services:**
```bash
docker-compose up --build
```

2. **Run migrations (first time):**
```bash
docker-compose exec web python manage.py migrate
```

3. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs/

### Production Docker Deployment

1. **Create production environment file:**
```bash
cp .env.example .env.production
```

2. **Edit `.env.production`:**
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/task_manager
```

3. **Build and run production containers:**
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🌐 Production Deployment

### Option 1: Traditional Server Deployment

#### Server Requirements
- Ubuntu 20.04+ / CentOS 8+ / Amazon Linux 2
- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Nginx
- Gunicorn

#### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib nginx -y

# Install Python dependencies
sudo apt install python3-dev libpq-dev build-essential -y
```

#### Step 2: Application Setup

```bash
# Create application user
sudo adduser taskmanager
sudo usermod -aG sudo taskmanager

# Clone repository
sudo -u taskmanager git clone <repository-url> /home/taskmanager/app
cd /home/taskmanager/app

# Create virtual environment
sudo -u taskmanager python3 -m venv venv
sudo -u taskmanager venv/bin/pip install -r requirements.txt

# Setup frontend
cd frontend
sudo -u taskmanager npm install
sudo -u taskmanager npm run build
cd ..
```

#### Step 3: Database Setup

```bash
# Create database user
sudo -u postgres createuser --interactive taskmanager

# Create database
sudo -u postgres createdb -O taskmanager taskmanager_prod

# Set up environment variables
sudo -u taskmanager cp .env.example .env
# Edit .env with production values
```

#### Step 4: Gunicorn Service

Create `/etc/systemd/system/taskmanager.service`:

```ini
[Unit]
Description=Task Manager Django Application
After=network.target

[Service]
User=taskmanager
Group=www-data
WorkingDirectory=/home/taskmanager/app
Environment="PATH=/home/taskmanager/app/venv/bin"
ExecStart=/home/taskmanager/app/venv/bin/gunicorn --workers 3 --bind unix:/home/taskmanager/app/taskmanager.sock task_manager.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable taskmanager
sudo systemctl start taskmanager
```

#### Step 5: Nginx Configuration

Create `/etc/nginx/sites-available/taskmanager`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/taskmanager/app;
    }
    
    location /media/ {
        root /home/taskmanager/app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/taskmanager/app/taskmanager.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Cloud Platform Deployment

#### Heroku Deployment

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create Heroku app:**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set environment variables:**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DJANGO_SETTINGS_MODULE=task_manager.settings
```

5. **Deploy:**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize application:**
```bash
eb init task-manager
```

3. **Create environment:**
```bash
eb create production
```

4. **Deploy:**
```bash
eb deploy
```

#### DigitalOcean App Platform

1. **Create app in DigitalOcean dashboard**
2. **Connect GitHub repository**
3. **Configure environment variables**
4. **Deploy**

## ⚙️ Environment Configuration

### Development Environment (.env)
```env
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Production Environment (.env.production)
```env
DEBUG=False
SECRET_KEY=your-very-secure-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/task_manager_prod
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## 🗄️ Database Setup

### PostgreSQL Production Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE task_manager_prod;
CREATE USER taskmanager WITH PASSWORD 'secure_password';
ALTER ROLE taskmanager SET client_encoding TO 'utf8';
ALTER ROLE taskmanager SET default_transaction_isolation TO 'read committed';
ALTER ROLE taskmanager SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE task_manager_prod TO taskmanager;
\q
```

### Database Backup Strategy

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/taskmanager"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U taskmanager task_manager_prod > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

## 📁 Static Files & Media

### Production Static Files Setup

```bash
# Collect static files
python manage.py collectstatic --noinput

# Set up permissions
sudo chown -R www-data:www-data /home/taskmanager/app/staticfiles
sudo chmod -R 755 /home/taskmanager/app/staticfiles
```

### Media Files Configuration

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# For production with cloud storage
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = 'your-access-key'
# AWS_SECRET_ACCESS_KEY = 'your-secret-key'
# AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
```

## 🔒 Security Considerations

### Essential Security Settings

```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Firewall Configuration

```bash
# UFW setup
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### SSL Certificate with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring & Logging

### Application Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/taskmanager/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Check Endpoint

```python
# views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U taskmanager -d task_manager_prod
```

#### 2. Static Files Not Loading
```bash
# Check permissions
ls -la staticfiles/

# Recollect static files
python manage.py collectstatic --noinput --clear
```

#### 3. Permission Denied Errors
```bash
# Fix file permissions
sudo chown -R www-data:www-data /home/taskmanager/app
sudo chmod -R 755 /home/taskmanager/app
```

#### 4. Gunicorn Not Starting
```bash
# Check logs
sudo journalctl -u taskmanager

# Restart service
sudo systemctl restart taskmanager
```

### Performance Optimization

1. **Database Optimization:**
   - Add database indexes
   - Use connection pooling
   - Optimize queries

2. **Caching:**
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **CDN for Static Files:**
   - Use AWS CloudFront or similar
   - Configure Django to use CDN URLs

### Backup and Recovery

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/taskmanager"

# Database backup
pg_dump -h localhost -U taskmanager task_manager_prod > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /home/taskmanager/app/media/

# Upload to cloud storage (optional)
# aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql s3://your-backup-bucket/
```

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Test database connectivity
4. Check firewall and security settings
5. Review this troubleshooting section

For additional support, create an issue in the repository or contact the development team.
