"""
News application models for managing users, articles, and publications.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model with role-based access control for the news application.
    
    This model extends Django's AbstractUser to provide role-based
    functionality for readers, journalists, and editors. It includes
    subscription management and content creation capabilities based on
    user roles.
    
    :param role: User role determining access permissions and capabilities
    :type role: str, choices=['reader', 'editor', 'journalist']
    :param publisher_subscriptions: Publishers that the user is subscribed to
    :type publisher_subscriptions: ManyToManyField to Publisher
    :param journalist_subscriptions: Journalists that the user is subscribed to
    :type journalist_subscriptions: ManyToManyField to self (User)
    :param independent_articles: Articles created independently by journalists
    :type independent_articles: ManyToManyField to Article
    :param independent_newsletters: Newsletters created independently by journalists
    :type independent_newsletters: ManyToManyField to Newsletter
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
        Check if the user has reader role.
        
        :return: True if user is a reader, False otherwise
        :rtype: bool
        """
        return self.role == 'reader'

    def is_editor(self):
        """
        Check if the user has editor role.
        
        :return: True if user is an editor, False otherwise
        :rtype: bool
        """
        return self.role == 'editor'

    def is_journalist(self):
        """
        Check if the user has journalist role.
        
        :return: True if user is a journalist, False otherwise
        :rtype: bool
        """
        return self.role == 'journalist'


class Publisher(models.Model):
    """
    Model representing a publication/publisher organization.
    
    Publishers manage their own journalists and editors, and can publish
    articles and newsletters. They have subscribers who receive content
    from their publications.
    
    :param name: Unique name of the publisher organization
    :type name: str, max_length=100, unique=True
    :param description: Detailed description of the publisher
    :type description: str, optional
    :param website: Official website URL of the publisher
    :type website: str, optional
    :param created_at: Timestamp when the publisher was created
    :type created_at: datetime, auto_now_add=True
    :param editors: Users with editor role associated with this publisher
    :type editors: ManyToManyField to User, filtered by role='editor'
    :param journalists: Users with journalist role associated with this publisher
    :type journalists: ManyToManyField to User, filtered by role='journalist'
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
    
    Articles go through a workflow from draft to published status, with
    role-based permissions for creation, editing, and approval.
    
    :param title: Headline of the article
    :type title: str, max_length=200
    :param content: Full text content of the article
    :type content: str
    :param summary: Brief summary of the article, max 500 characters
    :type summary: str, max_length=500, optional
    :param author: Journalist who created the article
    :type author: ForeignKey to User, filtered by role='journalist'
    :param publisher: Publisher organization associated with the article
    :type publisher: ForeignKey to Publisher, optional
    :param category: Article category for organization
    :type category: ForeignKey to Category, optional
    :param status: Current workflow status of the article
    :type status: str, choices=['draft', 'pending', 'approved', 'published', 'rejected']
    :param is_approved: Boolean flag indicating if article is approved
    :type is_approved: bool, default=False
    :param approved_by: Editor who approved the article
    :type approved_by: ForeignKey to User, filtered by role='editor', optional
    :param approved_at: Timestamp when article was approved
    :type approved_at: datetime, optional
    :param created_at: Timestamp when article was created
    :type created_at: datetime, auto_now_add=True
    :param updated_at: Timestamp when article was last modified
    :type updated_at: datetime, auto_now=True
    :param published_at: Timestamp when article was published
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
        Approve the article and update approval metadata.
        
        This method updates the article's approval status, sets the approving
        editor, and records the approval timestamp.
        
        :param editor: User with editor role who is approving the article
        :type editor: User, must have role='editor'
        :return: None
        :rtype: None
        :raises ValueError: If editor does not have editor role
        """
        if not editor.is_editor():
            raise ValueError("Only editors can approve articles")
        
        self.is_approved = True
        self.status = 'approved'
        self.approved_by = editor
        self.approved_at = timezone.now()
        self.save()


class Newsletter(models.Model):
    """
    Model representing a newsletter.
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
    Model for managing user subscriptions.
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
    Model for password reset tokens.
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
        """
        return not self.is_valid()
