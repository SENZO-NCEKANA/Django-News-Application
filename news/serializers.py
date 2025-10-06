"""
Serializers for news application REST API.
"""

from rest_framework import serializers
from .models import (
    User, Article, Publisher, Category, Newsletter, Subscription
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with role-based field access.
    
    This serializer handles serialization of User objects for API responses.
    It includes user identification, role information, and account status
    while maintaining security by excluding sensitive fields.
    
    :param id: User's unique identifier
    :type id: int
    :param username: User's unique username
    :type username: str
    :param email: User's email address
    :type email: str
    :param first_name: User's first name
    :type first_name: str
    :param last_name: User's last name
    :type last_name: str
    :param role: User's role (reader, editor, journalist)
    :type role: str
    :param date_joined: Account creation timestamp
    :type date_joined: datetime
    :param is_active: Account active status
    :type is_active: bool
    """
    class Meta:
        """
        Meta options for UserSerializer.
        """
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        """
        Meta options for CategorySerializer.
        """
        model = Category
        fields = ['id', 'name', 'description']


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for Publisher model.
    """
    class Meta:
        """
        Meta options for PublisherSerializer.
        """
        model = Publisher
        fields = [
            'id', 'name', 'description', 'website', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model with nested relationships.
    
    This serializer handles article serialization with nested user, publisher,
    and category information. It supports both read and write operations
    with proper field handling for API endpoints.
    
    :param author: Nested UserSerializer for article author information
    :type author: UserSerializer
    :param publisher: Nested PublisherSerializer for publisher information
    :type publisher: PublisherSerializer
    :param category: Nested CategorySerializer for category information
    :type category: CategorySerializer
    :param author_id: Write-only field for author ID assignment
    :type author_id: int
    :param publisher_id: Write-only field for publisher ID assignment
    :type publisher_id: int
    :param category_id: Write-only field for category ID assignment
    :type category_id: int
    """
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    publisher_id = serializers.IntegerField(write_only=True, required=False)
    category_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        """
        Meta options for ArticleSerializer.
        """
        model = Article
        fields = [
            'id', 'title', 'content', 'summary', 'author', 'publisher',
            'category', 'status', 'is_approved', 'created_at', 'updated_at',
            'published_at', 'author_id', 'publisher_id', 'category_id'
        ]
        read_only_fields = [
            'id', 'is_approved', 'created_at', 'updated_at', 'published_at'
        ]

    def create(self, validated_data):
        """
        Create article with proper author assignment.
        
        This method creates a new article instance with the provided
        validated data, handling author, publisher, and category
        relationships properly.
        
        :param validated_data: Dictionary of validated form data
        :type validated_data: dict
        :return: Created Article instance
        :rtype: Article
        """
        author_id = validated_data.pop('author_id')
        publisher_id = validated_data.pop('publisher_id', None)
        category_id = validated_data.pop('category_id', None)

        article = Article.objects.create(
            author_id=author_id,
            publisher_id=publisher_id,
            category_id=category_id,
            **validated_data
        )
        return article

    def update(self, instance, validated_data):
        """
        Update article with proper field handling.
        """
        author_id = validated_data.pop('author_id', None)
        publisher_id = validated_data.pop('publisher_id', None)
        category_id = validated_data.pop('category_id', None)

        if author_id:
            instance.author_id = author_id
        if publisher_id:
            instance.publisher_id = publisher_id
        if category_id:
            instance.category_id = category_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for Newsletter model.
    """
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    publisher_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        """
        Meta options for NewsletterSerializer.
        """
        model = Newsletter
        fields = [
            'id', 'title', 'content', 'author', 'publisher',
            'created_at', 'updated_at', 'author_id', 'publisher_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Create newsletter with proper author assignment.
        """
        author_id = validated_data.pop('author_id')
        publisher_id = validated_data.pop('publisher_id', None)

        newsletter = Newsletter.objects.create(
            author_id=author_id,
            publisher_id=publisher_id,
            **validated_data
        )
        return newsletter


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Subscription model.
    """
    user = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    journalist = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    publisher_id = serializers.IntegerField(write_only=True, required=False)
    journalist_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        """
        Meta class for Subscription model.
        """
        model = Subscription
        fields = [
            'id', 'user', 'publisher', 'journalist', 'created_at',
            'user_id', 'publisher_id', 'journalist_id'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """
        Validate that either publisher or journalist is selected.
        """
        publisher_id = data.get('publisher_id')
        journalist_id = data.get('journalist_id')

        if not publisher_id and not journalist_id:
            raise serializers.ValidationError(
                'Either publisher or journalist must be selected'
            )

        if publisher_id and journalist_id:
            raise serializers.ValidationError(
                'Cannot subscribe to both publisher and journalist'
            )

        return data

    def create(self, validated_data):
        """
        Create subscription with proper field assignment.
        """
        user_id = validated_data.pop('user_id')
        publisher_id = validated_data.pop('publisher_id', None)
        journalist_id = validated_data.pop('journalist_id', None)

        subscription = Subscription.objects.create(
            user_id=user_id,
            publisher_id=publisher_id,
            journalist_id=journalist_id,
            **validated_data
        )
        return subscription


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for article lists.
    """
    author_name = serializers.CharField(
        source='author.username', read_only=True
    )
    publisher_name = serializers.CharField(
        source='publisher.name', read_only=True
    )
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )

    class Meta:
        """
        Meta class for ArticleListSerializer.
        """
        model = Article
        fields = [
            'id', 'title', 'summary', 'author_name', 'publisher_name',
            'category_name', 'status', 'created_at', 'published_at'
        ]
