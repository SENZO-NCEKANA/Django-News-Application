"""
Configuration for the news application.
"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    Configuration for the news application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        """
        Initialize application when Django starts.

        This method is called when Django starts up and is used to
        register signal handlers and perform other initialization tasks.

        :return: None
        :rtype: None
        """
        # Import signals to register them
        try:
            import news.signals  # noqa: F401
        except ImportError:
            pass
