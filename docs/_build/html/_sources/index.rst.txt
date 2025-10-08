News Application Documentation
==============================

Welcome to the News Application documentation! This is a comprehensive Django-based news application that allows readers to view articles published by publishers and independent journalists, with role-based access control and subscription management.

Features
--------

User Roles
~~~~~~~~~~

- **Reader**: Can view published articles and manage subscriptions
- **Journalist**: Can create, edit, and manage articles and newsletters  
- **Editor**: Can review, approve, and manage articles from their publishers

Core Functionality
~~~~~~~~~~~~~~~~~~

- Article creation and management with approval workflow
- Publisher and journalist subscription system
- Email notifications when articles are approved
- Twitter integration for article sharing
- RESTful API for third-party integration
- Role-based access control and permissions

Technical Features
~~~~~~~~~~~~~~~~~~

- Custom User model with role-based fields
- Django signals for automated notifications
- Comprehensive unit testing
- PEP 8 compliant code
- Simple HTML templates with minimal styling

Quick Start
-----------

1. Install dependencies: ``pip install -r requirements.txt``
2. Run migrations: ``python manage.py migrate``
3. Set up groups: ``python manage.py setup_groups``
4. Create sample data: ``python manage.py create_sample_data``
5. Run server: ``python manage.py runserver``

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api

Models Documentation
--------------------

.. toctree::
   :maxdepth: 2

   models

Views Documentation
-------------------

.. toctree::
   :maxdepth: 2

   views

Forms Documentation
------------------

.. toctree::
   :maxdepth: 2

   forms

Serializers Documentation
------------------------

.. toctree::
   :maxdepth: 2

   serializers

Tests Documentation
-------------------

.. toctree::
   :maxdepth: 2

   tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`