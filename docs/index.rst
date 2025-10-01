News Application Documentation
==============================

Welcome to the News Application documentation. This Django-based news application provides a comprehensive platform for managing news articles, publishers, journalists, and readers with role-based access control.

Features
--------

* **Role-based Access Control**: Support for readers, journalists, and editors
* **Article Management**: Create, edit, approve, and publish articles
* **Publisher System**: Manage multiple publishers with their own journalists and editors
* **Subscription System**: Readers can subscribe to publishers or individual journalists
* **Newsletter System**: Journalists can create newsletters for their subscribers
* **REST API**: Full REST API support for all functionality
* **Search and Filtering**: Advanced search capabilities with category and publisher filtering

Getting Started
---------------

The application is built with Django and includes:

* Custom User model with role-based permissions
* Article management with approval workflow
* Publisher and journalist management
* Subscription system for readers
* REST API endpoints
* Email notifications for password reset

API Documentation
-----------------

The application provides a comprehensive REST API for all functionality. See the API documentation for detailed endpoint information.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   models
   views
   api
   forms
   management

