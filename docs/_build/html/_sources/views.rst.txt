Views Documentation
===================

This section documents all the Django views in the News Application.

Web Views
---------

.. automodule:: news.views
   :members:
   :undoc-members:
   :show-inheritance:

API Views
---------

.. automodule:: news.api_views
   :members:
   :undoc-members:
   :show-inheritance:

View Functions
~~~~~~~~~~~~~~

.. autofunction:: news.views.home

.. autofunction:: news.views.register

.. autofunction:: news.views.user_login

.. autofunction:: news.views.user_logout

.. autofunction:: news.views.article_list

.. autofunction:: news.views.article_detail

.. autofunction:: news.views.create_article

.. autofunction:: news.views.edit_article

.. autofunction:: news.views.approve_article

.. autofunction:: news.views.subscription_management

.. autofunction:: news.views.create_newsletter

.. autofunction:: news.views.search_articles

.. autofunction:: news.views.forgot_password

.. autofunction:: news.views.reset_password

API View Classes
~~~~~~~~~~~~~~~

.. autoclass:: news.api_views.ArticleListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.ArticleDetailAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.PublisherListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.CategoryListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.NewsletterListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.SubscriptionListAPIView
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: news.api_views.SubscriptionDetailAPIView
   :members:
   :undoc-members:
   :show-inheritance:

API Functions
~~~~~~~~~~~~~

.. autofunction:: news.api_views.approve_article_api

.. autofunction:: news.api_views.user_subscriptions_api
