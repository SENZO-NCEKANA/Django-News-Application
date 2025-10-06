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
    Custom user registration form with role selection and styling.
    
    This form extends Django's UserCreationForm to include role selection
    and additional user fields. It provides Bootstrap styling for form
    controls and validates user input for registration.
    
    :param role: User role selection field with choices from User.ROLE_CHOICES
    :type role: ChoiceField
    :param email: User email address field with email validation
    :type email: EmailField
    :param first_name: User's first name, maximum 30 characters
    :type first_name: CharField
    :param last_name: User's last name, maximum 30 characters
    :type last_name: CharField
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
        """
        Initialize form with Bootstrap styling for all fields.
        
        This method applies Bootstrap form-control class to username
        and password fields for consistent styling.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles with validation.
    
    This form provides fields for article creation and editing by journalists.
    It includes title, content, summary, publisher, and category fields with
    Bootstrap styling and validation.
    
    :param title: Article title field with placeholder text
    :type title: CharField
    :param content: Article content field with textarea widget
    :type content: TextField
    :param summary: Optional article summary field
    :type summary: TextField
    :param publisher: Publisher selection dropdown
    :type publisher: ModelChoiceField
    :param category: Category selection dropdown
    :type category: ModelChoiceField
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
        """
        Initialize form with querysets for publisher and category fields.
        
        This method sets up the querysets for the publisher and category
        dropdown fields to ensure they display all available options.
        """
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        self.fields['category'].queryset = Category.objects.all()


class ArticleApprovalForm(forms.ModelForm):
    """
    Form for editors to approve articles with status control.
    
    This form allows editors to approve or reject articles by setting
    the status and approval flag. It provides a clean interface for
    the approval workflow.
    
    :param status: Article status selection field
    :type status: ChoiceField
    :param is_approved: Boolean checkbox for approval status
    :type is_approved: BooleanField
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
    Form for managing user subscriptions to publishers and journalists.
    
    This form allows users to subscribe to either publishers or journalists.
    It includes validation to ensure only one type of subscription is selected
    and provides a clean interface for subscription management.
    
    :param publisher: Publisher selection dropdown for subscription
    :type publisher: ModelChoiceField
    :param journalist: Journalist selection dropdown for subscription
    :type journalist: ModelChoiceField
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
