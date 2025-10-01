API Documentation
==================

This section documents the REST API views and serializers in the news application.

API Views
---------

.. automodule:: news.api_views
   :members:
   :undoc-members:
   :show-inheritance:

Article API Views
-----------------

.. autoclass:: news.api_views.ArticleListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.ArticleDetailAPIView
   :members:
   :undoc-members:
   :show-inheritance:

Publisher and Category API Views
--------------------------------

.. autoclass:: news.api_views.PublisherListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.CategoryListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

Newsletter API Views
--------------------

.. autoclass:: news.api_views.NewsletterListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

Subscription API Views
----------------------

.. autoclass:: news.api_views.SubscriptionListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.SubscriptionDetailAPIView
   :members:
   :undoc-members:
   :show-inheritance:

API Functions
-------------

.. autofunction:: news.api_views.approve_article_api
.. autofunction:: news.api_views.user_subscriptions_api

Serializers
-----------

.. automodule:: news.serializers
   :members:
   :undoc-members:
   :show-inheritance:

User Serializer
---------------

.. autoclass:: news.serializers.UserSerializer
   :members:
   :undoc-members:
   :show-inheritance:

Article Serializers
------------------

.. autoclass:: news.serializers.ArticleSerializer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.serializers.ArticleListSerializer
   :members:
   :undoc-members:
   :show-inheritance:

Other Serializers
-----------------

.. autoclass:: news.serializers.CategorySerializer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.serializers.PublisherSerializer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.serializers.NewsletterSerializer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.serializers.SubscriptionSerializer
   :members:
   :undoc-members:
   :show-inheritance:
