"""
News application models for managing users, articles, and publications.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model with role-based fields for readers and journalists.

    This model extends Django's AbstractUser to provide role-based access
    control for a news application. Users can be readers, editors, or
    journalists, each with different permissions and capabilities.

    :param role: User role - one of 'reader', 'editor', or 'journalist',
        defaults to 'reader'
    :type role: str
    :param publisher_subscriptions: Many-to-many relationship to Publisher
        objects for reader subscriptions, defaults to empty
    :type publisher_subscriptions: ManyToManyField
    :param journalist_subscriptions: Many-to-many relationship to other User
        objects with journalist role for reader subscriptions, defaults to
        empty
    :type journalist_subscriptions: ManyToManyField
    :param independent_articles: Many-to-many relationship to Article objects
        for journalist's independent articles, defaults to empty
    :type independent_articles: ManyToManyField
    :param independent_newsletters: Many-to-many relationship to Newsletter
        objects for journalist's independent newsletters, defaults to empty
    :type independent_newsletters: ManyToManyField
    """
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='reader',
        validators=[MinLengthValidator(3)]
    )

    # Fields for readers
    publisher_subscriptions = models.ManyToManyField(
        'Publisher',
        related_name='subscribers',
        blank=True
    )
    journalist_subscriptions = models.ManyToManyField(
        'self',
        related_name='subscribers',
        blank=True,
        limit_choices_to={'role': 'journalist'}
    )

    # Fields for journalists
    independent_articles = models.ManyToManyField(
        'Article',
        related_name='independent_author',
        blank=True
    )
    independent_newsletters = models.ManyToManyField(
        'Newsletter',
        related_name='independent_author',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_reader(self):
        """
        Check if user has reader role.

        :return: True if user role is 'reader', False otherwise
        :rtype: bool
        """
        return self.role == 'reader'

    def is_editor(self):
        """
        Check if user has editor role.

        :return: True if user role is 'editor', False otherwise
        :rtype: bool
        """
        return self.role == 'editor'

    def is_journalist(self):
        """
        Check if user has journalist role.

        :return: True if user role is 'journalist', False otherwise
        :rtype: bool
        """
        return self.role == 'journalist'


class Publisher(models.Model):
    """
    Model representing a publication/publisher.

    This model represents a news publication or publisher that can have
    multiple editors and journalists associated with it. Publishers can
    have articles and newsletters created by their associated journalists.

    :param name: Publisher name, must be unique, defaults to None
    :type name: str
    :param description: Optional description of the publisher, defaults to
        empty
    :type description: str, optional
    :param website: Optional website URL for the publisher, defaults to
        empty
    :type website: str, optional
    :param created_at: Timestamp when publisher was created, auto-generated
    :type created_at: datetime
    :param editors: Many-to-many relationship to User objects with editor
        role, defaults to empty
    :type editors: ManyToManyField
    :param journalists: Many-to-many relationship to User objects with
        journalist role, defaults to empty
    :type journalists: ManyToManyField
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    editors = models.ManyToManyField(
        User,
        related_name='publisher_editors',
        limit_choices_to={'role': 'editor'}
    )
    journalists = models.ManyToManyField(
        User,
        related_name='publisher_journalists',
        limit_choices_to={'role': 'journalist'}
    )

    class Meta:
        """
        Meta options for Publisher model.
        """
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model for article categories.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        """
        Meta options for Category model.
        """
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Model representing a news article with approval workflow.

    This model represents a news article that can be created by journalists,
    reviewed by editors, and published to readers. Articles go through a
    status-based approval workflow from draft to published.

    :param title: Article title, maximum 200 characters, defaults to None
    :type title: str
    :param content: Full article content, defaults to None
    :type content: str
    :param summary: Optional article summary, maximum 500 characters,
        defaults to empty
    :type summary: str, optional
    :param author: Foreign key to User with journalist role who authored
        the article, required
    :type author: ForeignKey
    :param publisher: Foreign key to Publisher, can be null for independent
        articles, defaults to None
    :type publisher: ForeignKey, optional
    :param category: Foreign key to Category for article classification,
        can be null, defaults to None
    :type category: ForeignKey, optional
    :param status: Article status - one of 'draft', 'pending', 'approved',
        'published', 'rejected', defaults to 'draft'
    :type status: str
    :param is_approved: Boolean flag indicating if article is approved,
        defaults to False
    :type is_approved: bool
    :param approved_by: Foreign key to User with editor role who approved
        the article, can be null, defaults to None
    :type approved_by: ForeignKey, optional
    :param approved_at: Timestamp when article was approved, can be null,
        defaults to None
    :type approved_at: datetime, optional
    :param created_at: Timestamp when article was created, auto-generated
    :type created_at: datetime
    :param updated_at: Timestamp when article was last updated, auto-generated
    :type updated_at: datetime
    :param published_at: Timestamp when article was published, can be null,
        defaults to None
    :type published_at: datetime, optional
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_articles',
        limit_choices_to={'role': 'journalist'}
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='articles',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_articles',
        limit_choices_to={'role': 'editor'}
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """
        Meta class for Article model.
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def approve(self, editor):
        """
        Approve article by editor and update status to published.

        This method sets the article as approved, updates the status to
        'approved', records the approving editor and timestamp, then saves
        the changes.

        :param editor: User instance with editor role who approves the
            article
        :type editor: User
        :raises ValueError: If editor is not a valid User instance
        :raises AttributeError: If editor does not have editor role
        """
        self.is_approved = True
        self.status = 'approved'
        self.approved_by = editor
        self.approved_at = timezone.now()
        self.save()


class Newsletter(models.Model):
    """
    Model representing a newsletter created by journalists.

    This model represents a newsletter that can be created by journalists
    and associated with a publisher. Newsletters are typically sent to
    subscribers and contain curated content.

    :param title: Newsletter title, maximum 200 characters, defaults to
        None
    :type title: str
    :param content: Newsletter content, defaults to None
    :type content: str
    :param author: Foreign key to User with journalist role who authored
        the newsletter, required
    :type author: ForeignKey
    :param publisher: Foreign key to Publisher, can be null for independent
        newsletters, defaults to None
    :type publisher: ForeignKey, optional
    :param created_at: Timestamp when newsletter was created, auto-generated
    :type created_at: datetime
    :param updated_at: Timestamp when newsletter was last updated,
        auto-generated
    :type updated_at: datetime
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_newsletters',
        limit_choices_to={'role': 'journalist'}
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='newsletters',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Newsletter model.
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """
    Model for managing user subscriptions to publishers and journalists.

    This model represents a subscription relationship between a user and
    either a publisher or a journalist. Users can subscribe to receive
    content from specific publishers or follow individual journalists.

    :param user: Foreign key to User who is subscribing, required
    :type user: ForeignKey
    :param publisher: Foreign key to Publisher being subscribed to, can be
        null if subscribing to journalist instead, defaults to None
    :type publisher: ForeignKey, optional
    :param journalist: Foreign key to User with journalist role being
        subscribed to, can be null if subscribing to publisher instead,
        defaults to None
    :type journalist: ForeignKey, optional
    :param created_at: Timestamp when subscription was created, auto-generated
    :type created_at: datetime
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    journalist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subscribed_to_journalist',
        limit_choices_to={'role': 'journalist'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for Subscription model.
        """
        unique_together = [
            ('user', 'publisher'),
            ('user', 'journalist')
        ]

    def __str__(self):
        if self.publisher:
            return f"{self.user} subscribes to {self.publisher}"
        return f"{self.user} subscribes to {self.journalist}"


class PasswordResetToken(models.Model):
    """
    Model for password reset tokens with expiration and usage tracking.

    This model represents a secure token used for password reset
    functionality. Tokens are time-limited (24 hours) and can only be
    used once to prevent security vulnerabilities.

    :param user: Foreign key to User requesting password reset, required
    :type user: ForeignKey
    :param token: Unique token string for password reset, maximum 100
        characters, defaults to None
    :type token: str
    :param created_at: Timestamp when token was created, auto-generated
    :type created_at: datetime
    :param is_used: Boolean flag indicating if token has been used,
        defaults to False
    :type is_used: bool
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for PasswordResetToken model.
        """
        ordering = ['-created_at']

    def __str__(self):
        return f"Password reset token for {self.user.username}"

    def is_valid(self):
        """
        Check if token is valid (not used and not expired).

        Returns:
            bool: True if token is valid and not expired, False otherwise
        """
        from datetime import timedelta

        if self.is_used:
            return False

        # Token expires after 24 hours
        expiry_time = self.created_at + timedelta(hours=24)
        return timezone.now() < expiry_time

    def is_expired(self):
        """
        Check if token is expired.

        Returns:
            bool: True if token is expired, False otherwise
        """
        return not self.is_valid()
