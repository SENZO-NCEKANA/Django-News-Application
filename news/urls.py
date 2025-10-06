"""
URL configuration for news application.
"""

from django.urls import path, include
from . import views

app_name = 'news'

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password,
         name='reset_password'),

    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:pk>/approve/', views.approve_article,
         name='approve_article'),

    # Subscriptions
    path('subscriptions/', views.subscription_management,
         name='subscription_management'),
    path('subscriptions/<int:pk>/delete/', views.delete_subscription,
         name='delete_subscription'),

    # Newsletters
    path('newsletters/create/', views.create_newsletter,
         name='create_newsletter'),

    # Search
    path('search/', views.search_articles, name='search_articles'),

    # API
    path('api/', include('news.api_urls')),
]
