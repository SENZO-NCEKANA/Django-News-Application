API Documentation
==================

This section documents the REST API endpoints in the News Application.

API Overview
------------

The News Application provides a comprehensive REST API for managing articles, users, subscriptions, and more. All API endpoints require authentication using token-based authentication.

Authentication
~~~~~~~~~~~~~

All API endpoints require authentication. Include the token in the Authorization header:

.. code-block:: http

   Authorization: Token your-token-here

Endpoints
---------

Articles
~~~~~~~~

.. http:get:: /api/articles/

   List articles based on user role and subscriptions.

   **Response:** List of articles with nested author, publisher, and category information.

.. http:post:: /api/articles/

   Create a new article (journalists only).

   **Request Body:**
   
   .. code-block:: json

      {
          "title": "Article Title",
          "content": "Article content...",
          "summary": "Article summary",
          "author_id": 1,
          "publisher_id": 1,
          "category_id": 1
      }

.. http:get:: /api/articles/{id}/

   Retrieve a specific article.

.. http:put:: /api/articles/{id}/

   Update an article (author or editors only).

.. http:delete:: /api/articles/{id}/

   Delete an article (author or editors only).

.. http:post:: /api/articles/{id}/approve/

   Approve an article (editors only).

Publishers
~~~~~~~~~~

.. http:get:: /api/publishers/

   List all publishers.

Categories
~~~~~~~~~~

.. http:get:: /api/categories/

   List all categories.

Newsletters
~~~~~~~~~~~

.. http:get:: /api/newsletters/

   List newsletters based on user subscriptions.

.. http:post:: /api/newsletters/

   Create a new newsletter (journalists only).

Subscriptions
~~~~~~~~~~~~~

.. http:get:: /api/subscriptions/

   List user's subscriptions.

.. http:post:: /api/subscriptions/

   Create a new subscription.

.. http:get:: /api/subscriptions/{id}/

   Retrieve a specific subscription.

.. http:delete:: /api/subscriptions/{id}/

   Delete a subscription.

User Subscriptions
~~~~~~~~~~~~~~~~~~

.. http:get:: /api/user-subscriptions/

   Get user's subscribed content (readers only).

   **Response:**
   
   .. code-block:: json

      {
          "publishers": [...],
          "journalists": [...],
          "articles": [...]
      }

Error Responses
~~~~~~~~~~~~~~~

All endpoints may return the following error responses:

.. code-block:: json

   {
       "detail": "Authentication credentials were not provided."
   }

.. code-block:: json

   {
       "detail": "You do not have permission to perform this action."
   }

.. code-block:: json

   {
       "field_name": ["This field is required."]
   }
