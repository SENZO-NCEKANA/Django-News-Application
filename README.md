# Django News Application

A Django news application where users can read articles from publishers and journalists. Features user roles, subscriptions, and article management.

## Features

### User Roles
- **Reader**: Can view published articles and manage subscriptions
- **Journalist**: Can create, edit, and manage articles and newsletters  
- **Editor**: Can review, approve, and manage articles from their publishers

### Core Functionality
- Create and manage articles with approval process
- Subscribe to publishers and journalists
- Email notifications for approved articles
- Share articles on Twitter
- REST API for integration
- User permissions and access control

### Technical Features
- User roles and permissions
- Email notifications
- Testing
- HTML templates
- Docker support

## Setup

### Using Docker

#### Requirements
- Docker and Docker Compose
- Git

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/SENZO-NCEKANA/Django-News-Application.git
   cd django-news-application
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Go to `http://localhost:8000`
   - Admin login: `admin` / `admin123`

#### Docker Commands
```bash
# Start the application
docker-compose up --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose up --build --force-recreate
```

### Using Python Virtual Environment

#### Requirements
- Python 3.8+
- MySQL or MariaDB
- Git

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/SENZO-NCEKANA/Django-News-Application.git
   cd django-news-application
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   
   **For MySQL/MariaDB:**
   ```bash
   # Start MySQL service
   # On macOS with Homebrew:
   brew services start mariadb
   
   # On Ubuntu/Debian:
   sudo systemctl start mysql
   
   # Create database
   mysql -u root -p
   CREATE DATABASE news_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

5. **Configure database settings**
   
   Edit `news_app/settings.py` and update the database configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'news_app_db',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',  # Update this
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
               'charset': 'utf8mb4',
           },
       }
   }
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Set up user groups and sample data**
   ```bash
   python manage.py setup_groups
   python manage.py create_sample_data
   ```

8. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Open your browser and go to `http://127.0.0.1:8000/`

## Environment Variables

For production deployment, set these environment variables:

### Required Variables
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Variables (for Docker)
- `MYSQL_DATABASE`: Database name (default: `news_app_db`)
- `MYSQL_USER`: Database user (default: `newsuser`)
- `MYSQL_PASSWORD`: Database password (default: `newspassword`)
- `DB_HOST`: Database host (default: `db`)

### Email Configuration
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `EMAIL_USE_TLS`: Use TLS (True/False)

### Twitter Integration (Optional)
- `TWITTER_API_KEY`: Twitter API key
- `TWITTER_API_SECRET`: Twitter API secret
- `TWITTER_ACCESS_TOKEN`: Twitter access token
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter access token secret
- `TWITTER_ENABLED`: Enable Twitter posting (True/False)

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit secrets to version control**
   - Add sensitive files to `.gitignore`
   - Use environment variables for secrets
   - Use `.env` files for local development (not tracked in git)

2. **Production deployment**
   - Change the default `SECRET_KEY`
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`
   - Use HTTPS in production
   - Use a production WSGI server (gunicorn, uWSGI)

3. **Database security**
   - Use strong database passwords
   - Restrict database access to application servers only
   - Regular database backups

## API Documentation

The application includes a comprehensive REST API. Access the API documentation at:
- `http://localhost:8000/api/` (when running locally)
- Full API documentation is available in the `docs/` directory

### API Endpoints
- `GET /api/articles/` - List articles
- `POST /api/articles/` - Create article (journalists only)
- `GET /api/articles/{id}/` - Retrieve article
- `PUT /api/articles/{id}/` - Update article
- `POST /api/articles/{id}/approve/` - Approve article (editors only)
- `GET /api/publishers/` - List publishers
- `GET /api/categories/` - List categories
- `GET /api/newsletters/` - List newsletters
- `POST /api/subscriptions/` - Create subscription

## Testing

Run the test suite:
```bash
python manage.py test
```

The test suite includes:
- Model tests for all database models
- View tests for authentication and authorization
- API tests for REST endpoints
- Email notification tests

## Documentation

See the `docs/` folder for documentation.

## Project Structure

```
django-news-application/
├── news/                    # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # Web views
│   ├── api_views.py        # REST API views
│   ├── serializers.py      # API serializers
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin configuration
│   ├── signals.py          # Django signals
│   ├── tests.py            # Unit tests
│   ├── management/         # Management commands
│   └── templates/          # HTML templates
├── news_app/               # Django project settings
│   ├── settings.py         # Main settings
│   ├── settings_docker.py  # Docker-specific settings
│   └── urls.py            # URL configuration
├── docs/                   # Sphinx documentation
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## About

This project was built as part of a Capstone Project – Consolidation Task.