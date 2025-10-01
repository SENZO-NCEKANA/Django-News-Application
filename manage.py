#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This module provides the entry point for Django management commands
for the News Application. It handles command-line argument parsing
and execution of Django administrative tasks such as:

- Running the development server (runserver)
- Database migrations (migrate, makemigrations)
- Creating superusers (createsuperuser)
- Collecting static files (collectstatic)
- Running tests (test)
- Custom management commands (create_sample_data, setup_groups)

The module sets up the Django environment and delegates command
execution to Django's core management framework.
"""
import os
import sys


def main():
    """
    Execute Django management commands for the news application.

    This function serves as the entry point for Django's command-line utility,
    handling administrative tasks such as running the development server,
    database migrations, and other Django management operations.

    Sets the default Django settings module and executes command-line
    arguments through Django's management framework with proper error
    handling for import issues.

    :return: None
    :rtype: None
    :raises ImportError: If Django is not installed or virtual environment
        is not activated
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
