"""
Views for news application with role-based access control.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    User, Article, Publisher, Category, Subscription, PasswordResetToken
)
from .forms import (
    UserRegistrationForm, ArticleForm, NewsletterForm,
    SubscriptionForm, ArticleApprovalForm, ForgotPasswordForm,
    ResetPasswordForm
)


def home(request):
    """
    Home page displaying recent articles.

    Args:
        request: HTTP request object

    Returns:
        HttpResponse: Rendered home page with recent articles
    """
    articles = Article.objects.filter(
        status='published'
    ).select_related('author', 'publisher', 'category')

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'news/home.html', context)


def register(request):
    """
    User registration view with role selection.

    Args:
        request: HTTP request object

    Returns:
        HttpResponse: Registration form or redirect after successful
            registration
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Account created successfully for {user.username}'
            )
            return redirect('news:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    """
    User login view.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('news:home')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'news/login.html')


@login_required
def user_logout(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('news:home')


@login_required
def article_list(request):
    """
    Article list view with role-based filtering.
    """
    articles = Article.objects.all()

    if request.user.is_reader():
        articles = articles.filter(status='published')
    elif request.user.is_journalist():
        articles = articles.filter(author=request.user)
    elif request.user.is_editor():
        articles = articles.filter(
            Q(publisher__editors=request.user) | Q(status='pending')
        )

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'user_role': request.user.role,
    }
    return render(request, 'news/article_list.html', context)


@login_required
def article_detail(request, pk):
    """
    Article detail view.
    """
    article = get_object_or_404(Article, pk=pk)

    if request.user.is_reader() and article.status != 'published':
        messages.error(request, 'This article is not published yet')
        return redirect('news:article_list')

    context = {'article': article}
    return render(request, 'news/article_detail.html', context)


@login_required
def create_article(request):
    """
    Create article view for journalists.
    """
    if not request.user.is_journalist():
        messages.error(request, 'Only journalists can create articles')
        return redirect('news:article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created successfully')
            return redirect('news:article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return render(request, 'news/create_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    """
    Edit article view for journalists and editors.
    """
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or
            request.user.is_editor()):
        messages.error(
            request,
            'You do not have permission to edit this article'
        )
        return redirect('news:article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully')
            return redirect('news:article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {'form': form, 'article': article}
    return render(request, 'news/edit_article.html', context)


@login_required
def approve_article(request, pk):
    """
    Article approval view for editors.
    """
    if not request.user.is_editor():
        messages.error(request, 'Only editors can approve articles')
        return redirect('news:article_list')

    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleApprovalForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.approve(request.user)
            article.save()
            messages.success(request, 'Article approved successfully')
            return redirect('news:article_detail', pk=article.pk)
    else:
        form = ArticleApprovalForm(instance=article)

    context = {'form': form, 'article': article}
    return render(request, 'news/approve_article.html', context)


@login_required
def subscription_management(request):
    """
    Subscription management view for readers.
    """
    if not request.user.is_reader():
        messages.error(request, 'Only readers can manage subscriptions')
        return redirect('news:home')

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user

            # Use get_or_create to handle duplicates gracefully
            if subscription.publisher:
                sub, created = Subscription.objects.get_or_create(
                    user=request.user,
                    publisher=subscription.publisher,
                    defaults={'journalist': None}
                )
                if created:
                    messages.success(
                        request,
                        f'Successfully subscribed to '
                        f'{subscription.publisher.name}'
                    )
                else:
                    messages.warning(
                        request,
                        f'You are already subscribed to '
                        f'{subscription.publisher.name}'
                    )
            elif subscription.journalist:
                sub, created = Subscription.objects.get_or_create(
                    user=request.user,
                    journalist=subscription.journalist,
                    defaults={'publisher': None}
                )
                if created:
                    messages.success(
                        request,
                        f'Successfully subscribed to '
                        f'{subscription.journalist.username}'
                    )
                else:
                    messages.warning(
                        request,
                        f'You are already subscribed to '
                        f'{subscription.journalist.username}'
                    )

            return redirect('news:subscription_management')
    else:
        form = SubscriptionForm()

    subscriptions = Subscription.objects.filter(user=request.user)

    context = {
        'form': form,
        'subscriptions': subscriptions,
    }
    return render(request, 'news/subscription_management.html', context)


@login_required
def delete_subscription(request, pk):
    """
    Delete subscription view.
    """
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    if request.method == 'POST':
        subscription.delete()
        messages.success(request, 'Subscription removed successfully')
        return redirect('news:subscription_management')

    context = {'subscription': subscription}
    return render(request, 'news/delete_subscription.html', context)


@login_required
def create_newsletter(request):
    """
    Create newsletter view for journalists.
    """
    if not request.user.is_journalist():
        messages.error(request, 'Only journalists can create newsletters')
        return redirect('news:home')

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, 'Newsletter created successfully')
            return redirect('news:home')
    else:
        form = NewsletterForm()

    return render(request, 'news/create_newsletter.html', {'form': form})


def search_articles(request):
    """
    Search articles view.
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    publisher = request.GET.get('publisher', '')

    articles = Article.objects.filter(status='published')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if category:
        articles = articles.filter(category__name=category)

    if publisher:
        articles = articles.filter(publisher__name=publisher)

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': Category.objects.all(),
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'news/search_results.html', context)


def forgot_password(request):
    """
    Handle password reset request.
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)

                # Generate token for password reset
                import secrets
                token = secrets.token_urlsafe(32)

                # Create password reset token
                PasswordResetToken.objects.create(
                    user=user,
                    token=token
                )

                # Send email with reset link
                from django.core.mail import send_mail
                from django.conf import settings

                reset_url = request.build_absolute_uri(
                    f'/reset-password/{token}/'
                )

                try:
                    send_mail(
                        'Password Reset Request',
                        f'Click the link to reset your password: {reset_url}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    # Log the error but don't expose it to the user
                    print(f"Email sending failed: {e}")
                    # Still show success message for security

                messages.success(
                    request,
                    'Password reset link sent to your email.'
                )
                return redirect('news:login')

            except User.DoesNotExist:
                messages.error(
                    request,
                    'No account found with that email address.'
                )
    else:
        form = ForgotPasswordForm()

    return render(request, 'news/forgot_password.html', {'form': form})


def reset_password(request, token):
    """
    Handle password reset with token.
    """
    try:
        reset_token = PasswordResetToken.objects.get(token=token)

        if not reset_token.is_valid():
            messages.error(request, 'Invalid or expired reset token.')
            return redirect('news:forgot_password')

        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                reset_token.user.set_password(new_password)
                reset_token.user.save()

                # Mark token as used
                reset_token.is_used = True
                reset_token.save()

                messages.success(
                    request,
                    'Password reset successfully. Please log in.'
                )
                return redirect('news:login')
        else:
            form = ResetPasswordForm()

        return render(
            request,
            'news/reset_password.html',
            {'form': form, 'token': token}
        )

    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset token.')
        return redirect('news:forgot_password')
