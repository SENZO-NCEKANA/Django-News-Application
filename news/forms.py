"""
Forms for news application with validation and user-friendly interfaces.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Article, Publisher, Category, Newsletter, Subscription
)


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form with role-based account creation.
    
    Extends Django's UserCreationForm to include role selection and additional
    user fields. Provides form validation and user-friendly interface for
    account registration with role-based access control.
    
    :param role: User role selection (reader, editor, journalist)
    :type role: ChoiceField, choices=User.ROLE_CHOICES
    :param email: User email address for account
    :type email: EmailField
    :param first_name: User's first name
    :type first_name: CharField, max_length=30
    :param last_name: User's last name
    :type last_name: CharField, max_length=30
    """
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        """
        Meta options for UserRegistrationForm.
        """
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'role', 'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles with validation.
    
    Provides a user-friendly interface for journalists to create and edit
    articles with proper field validation and widget customization.
    
    :param title: Article headline with placeholder text
    :type title: TextInput widget with form-control class
    :param content: Article body text with textarea widget
    :type content: Textarea widget, 10 rows, form-control class
    :param summary: Optional article summary with textarea widget
    :type summary: Textarea widget, 3 rows, form-control class
    :param publisher: Publisher selection dropdown
    :type publisher: Select widget with form-control class
    :param category: Category selection dropdown
    :type category: Select widget with form-control class
    """
    class Meta:
        """
        Meta options for ArticleForm.
        """
        model = Article
        fields = [
            'title', 'content', 'summary', 'publisher', 'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter article content'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter article summary (optional)'
            }),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        self.fields['category'].queryset = Category.objects.all()


class ArticleApprovalForm(forms.ModelForm):
    """
    Form for editors to approve articles.
    """
    class Meta:
        """
        Meta options for ArticleApprovalForm.
        """
        model = Article
        fields = ['status', 'is_approved']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }


class NewsletterForm(forms.ModelForm):
    """
    Form for creating newsletters.
    """
    class Meta:
        """
        Meta options for NewsletterForm.
        """
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter newsletter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter newsletter content'
            }),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()


class SubscriptionForm(forms.ModelForm):
    """
    Form for managing subscriptions.
    """
    class Meta:
        """
        Meta options for SubscriptionForm.
        """
        model = Subscription
        fields = ['publisher', 'journalist']
        widgets = {
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'journalist': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        self.fields['journalist'].queryset = User.objects.filter(
            role='journalist'
        )
        self.fields['publisher'].required = False
        self.fields['journalist'].required = False

    def clean(self):
        cleaned_data = super().clean()
        publisher = cleaned_data.get('publisher')
        journalist = cleaned_data.get('journalist')

        if not publisher and not journalist:
            raise forms.ValidationError(
                'You must subscribe to either a publisher or a journalist.'
            )

        return cleaned_data


class SearchForm(forms.Form):
    """
    Form for searching articles.
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search articles...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        empty_label="All Publishers",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ForgotPasswordForm(forms.Form):
    """
    Form for requesting password reset.
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )


class ResetPasswordForm(forms.Form):
    """
    Form for resetting password with token.
    """
    new_password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return cleaned_data
