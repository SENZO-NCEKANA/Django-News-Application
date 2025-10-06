# Docker Deployment Guide

This guide explains how to run the News Application using Docker.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **If you have the project files locally:**
   ```bash
   # Navigate to the project directory
   cd /path/to/News-Application-2
   
   # Start the application
   docker-compose up --build
   ```

2. **If using Docker Playground:**
   ```bash
   # Upload the news-app-docker.zip file to Docker Playground
   # Extract it and navigate to the directory
   unzip news-app-docker.zip
   cd news-app-docker
   
   # Start the application
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin credentials: `admin` / `admin123`

### Option 2: Using Docker only

1. **Build the Docker image**
   ```bash
   docker build -t news-app .
   ```

2. **Run the container with SQLite (for testing)**
   ```bash
   docker run -p 8000:8000 news-app
   ```

## Docker Compose Services

- **web**: Django application server
- **db**: MySQL 8.0 database server

## Environment Variables

You can customize the deployment using these environment variables:

- `DEBUG`: Set to `True` for development (default: `False`)
- `MYSQL_DATABASE`: Database name (default: `news_app_db`)
- `MYSQL_USER`: Database user (default: `newsuser`)
- `MYSQL_PASSWORD`: Database password (default: `newspassword`)
- `SECRET_KEY`: Django secret key (change in production)

## Production Deployment

For production deployment:

1. **Set environment variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DEBUG=False
   ```

2. **Use production database**
   - Update `docker-compose.yml` to use external database
   - Configure proper `ALLOWED_HOSTS` in settings

3. **Use production WSGI server**
   - Replace `runserver` with `gunicorn` in Dockerfile
   - Add nginx reverse proxy

## Docker Playground

This application is compatible with Docker Playground:

1. Copy the project files to Docker Playground
2. Run `docker-compose up --build`
3. Access the application via the provided URL

## Troubleshooting

### Database Connection Issues
- Ensure the database service is healthy before starting the web service
- Check database credentials in environment variables

### Port Conflicts
- Change the port mapping in `docker-compose.yml` if port 8000 is in use
- Update the `EXPOSE` directive in Dockerfile if needed

### Permission Issues
- The application runs as a non-root user for security
- Ensure proper file permissions for the application directory

## Development

For development with live code reloading:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Health Checks

The application includes health checks to ensure proper startup:
- Database connectivity check
- HTTP endpoint availability check
- Automatic retry on failure

## Logs

View application logs:
```bash
docker-compose logs -f web
```

View database logs:
```bash
docker-compose logs -f db
```
