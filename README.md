# Django News Application

A comprehensive Django-based news application with role-based access control, featuring publishers, journalists, editors, and readers. The application includes a REST API, subscription system, and newsletter functionality.

## Features

- **Role-based Access Control**: Support for readers, journalists, and editors
- **Article Management**: Create, edit, approve, and publish articles
- **Publisher System**: Manage multiple publishers with their own journalists and editors
- **Subscription System**: Readers can subscribe to publishers or individual journalists
- **Newsletter System**: Journalists can create newsletters for their subscribers
- **REST API**: Full REST API support for all functionality
- **Search and Filtering**: Advanced search capabilities with category and publisher filtering
- **Email Notifications**: Password reset and article notifications
- **Docker Support**: Containerized deployment ready

## Prerequisites

- Python 3.11+
- MySQL 8.0+ (optional, SQLite supported for development)
- Docker and Docker Compose (for containerized deployment)

## Installation

### Option 1: Virtual Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd News-Application-2
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Copy the environment template and create a `.env` file:
   ```bash
   cp env.template .env
   ```
   Then edit `.env` with your actual values:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=mysql://username:password@localhost:3306/news_app
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   TWITTER_BEARER_TOKEN=your-twitter-token
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd News-Application-2
   ```

2. **Configure environment variables**
   Copy the environment template and create a `.env` file:
   ```bash
   cp env.template .env
   ```
   Then edit `.env` with your actual values:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=mysql://news_user:news_password@db:3306/news_app
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   docker-compose exec web python manage.py create_sample_data
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection URL | SQLite |
| `EMAIL_HOST_USER` | SMTP username | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | - |
| `TWITTER_BEARER_TOKEN` | Twitter API token | - |

### Database Configuration

The application supports both MySQL and SQLite:

- **MySQL**: Set `DATABASE_URL=mysql://user:password@host:port/database`
- **SQLite**: Default fallback for development

### Email Configuration

For production, configure SMTP settings:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Usage

### User Roles

1. **Readers**: Can view published articles, subscribe to publishers/journalists
2. **Journalists**: Can create articles and newsletters, manage their content
3. **Editors**: Can approve articles, manage publishers and journalists

### API Endpoints

The application provides a comprehensive REST API:

- **Articles**: `/api/articles/`
- **Publishers**: `/api/publishers/`
- **Categories**: `/api/categories/`
- **Newsletters**: `/api/newsletters/`
- **Subscriptions**: `/api/subscriptions/`

### Management Commands

- `python manage.py create_sample_data`: Create sample data for testing
- `python manage.py setup_groups`: Set up user groups and permissions

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **HTML Documentation**: Open `docs/_build/html/index.html` in your browser
- **API Documentation**: Detailed REST API documentation
- **Model Documentation**: Database models and relationships
- **View Documentation**: All view functions and their purposes

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

The project follows PEP 8 style guidelines:
- Line length: 79 characters maximum
- Comprehensive docstrings
- Type hints where appropriate

### Pre-commit Hooks (Optional)

To set up pre-commit hooks for code quality:

```bash
pip install pre-commit
pre-commit install
```

## Deployment

### Production Settings

For production deployment:

1. Set `DEBUG=False`
2. Configure proper `SECRET_KEY`
3. Set up production database
4. Configure static file serving
5. Set up email backend
6. Configure `ALLOWED_HOSTS`

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Security Considerations

- Never commit secrets to version control
- Use environment variables for sensitive data
- Configure proper CORS settings
- Set up HTTPS in production
- Regular security updates

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure database credentials are correct
2. **Static Files**: Run `python manage.py collectstatic`
3. **Migrations**: Run `python manage.py migrate`
4. **Permissions**: Check file permissions for media/static directories

### Docker Issues

1. **Port Conflicts**: Change ports in docker-compose.yml
2. **Database Connection**: Ensure database service is healthy
3. **Volume Mounts**: Check volume permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.

---

**Note**: This application is designed for educational and development purposes. For production use, ensure proper security configurations and follow Django security best practices.