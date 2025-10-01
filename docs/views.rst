Views Documentation
===================

This section documents all the Django views in the news application.

.. automodule:: news.views
   :members:
   :undoc-members:
   :show-inheritance:

Home View
---------

.. autofunction:: news.views.home

Registration and Authentication
------------------------------

.. autofunction:: news.views.register
.. autofunction:: news.views.user_login
.. autofunction:: news.views.user_logout

Article Management
------------------

.. autofunction:: news.views.article_list
.. autofunction:: news.views.article_detail
.. autofunction:: news.views.create_article
.. autofunction:: news.views.edit_article
.. autofunction:: news.views.approve_article

Subscription Management
----------------------

.. autofunction:: news.views.subscription_management
.. autofunction:: news.views.delete_subscription

Newsletter Management
---------------------

.. autofunction:: news.views.create_newsletter

Search and Password Reset
-------------------------

.. autofunction:: news.views.search_articles
.. autofunction:: news.views.forgot_password
.. autofunction:: news.views.reset_password
