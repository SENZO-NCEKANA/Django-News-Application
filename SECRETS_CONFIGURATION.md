# Secrets Configuration Guide

This file provides guidance on configuring secrets for the Django News Application. **This file should be removed after review as it contains sensitive information.**

## Required Environment Variables

### 1. Django Secret Key
```env
SECRET_KEY=your-very-secure-secret-key-here
```
**How to generate**: Use Django's built-in key generator:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Database Configuration

#### For MySQL/MariaDB:
```env
DATABASE_URL=mysql://username:password@host:port/database_name
```

#### For PostgreSQL:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

#### For SQLite (Development):
```env
# No DATABASE_URL needed - will use SQLite by default
```

### 3. Email Configuration

#### Gmail SMTP:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

**Note**: For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an App Password (not your regular password)
3. Use the App Password in EMAIL_HOST_PASSWORD

#### Other SMTP Providers:
```env
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-password
```

### 4. Twitter API (Optional)
```env
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
```

To get a Twitter Bearer Token:
1. Go to https://developer.twitter.com/
2. Create a new app
3. Generate Bearer Token
4. Use the token in your environment variables

### 5. Production Settings

#### Debug Mode:
```env
DEBUG=False
```

#### Allowed Hosts:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost
```

## Environment File Setup

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=mysql://username:password@localhost:3306/news_app

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Twitter API (Optional)
TWITTER_BEARER_TOKEN=your-twitter-token
```

## Docker Environment Variables

For Docker deployment, create a `.env` file or set environment variables:

```bash
# Using .env file
docker-compose up

# Or set environment variables directly
export SECRET_KEY="your-secret-key"
export DATABASE_URL="mysql://user:pass@db:3306/news_app"
docker-compose up
```

## Security Best Practices

1. **Never commit secrets to version control**
2. **Use different secrets for development and production**
3. **Rotate secrets regularly**
4. **Use environment variables, not hardcoded values**
5. **Consider using a secrets management service for production**

## Example Production Configuration

```env
# Production Environment Variables
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=mysql://prod_user:secure_password@db_host:3306/news_app_prod
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Testing Configuration

For testing, you can use these example values:

```env
SECRET_KEY=django-insecure-test-key-for-development-only
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=test@example.com
EMAIL_HOST_PASSWORD=test-password
```

---

**⚠️ IMPORTANT**: This file contains sensitive information and should be removed after the review process is complete. Never commit actual secrets to version control.
