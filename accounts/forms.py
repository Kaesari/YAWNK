from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model

# ======================================
# SPLIT FORMS FOR SETTINGS PAGE
# ======================================

class CustomUserCreationForm(UserCreationForm):
    """Simplified signup form with only essential fields"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    
    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'bio', 'location', 'profile_picture')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254 700 000 000'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address, city, postal code'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something about yourself'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password field from the form (inherited from UserChangeForm)
        if 'password' in self.fields:
            del self.fields['password']
        
        # Make fields optional (not required)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['address'].required = False
    
    def clean_username(self):
        """
        Validate that the username is unique (excluding current user)
        """
        username = self.cleaned_data.get('username')
        User = get_user_model()
        
        # Get the current user instance being edited
        current_user = self.instance
        
        # Check if username is being changed
        if current_user and current_user.username == username:
            # Username hasn't changed, allow it
            return username
        
        # Check if username is taken by another user
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        
        return username


# ======================================
# SPLIT FORMS FOR SETTINGS PAGE
# Prevents data overwriting between sections
# ======================================

class ProfileDetailsForm(forms.ModelForm):
    """Form for editing profile picture, username, location, and bio (Public Info)"""
    
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'username', 'location', 'bio')
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Nairobi, Kenya'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell others about yourself...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    
    def clean_username(self):
        """Validate that the username is unique (excluding current user)"""
        username = self.cleaned_data.get('username')
        current_user = self.instance
        
        # Check if username is being changed
        if current_user and current_user.username == username:
            return username
        
        # Check if username is taken by another user
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another.')
        
        return username


class AccountDetailsForm(forms.ModelForm):
    """Form for editing first name, last name, email, phone, and address (Private Info)"""
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254 700 000 000'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address, city, postal code'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional (not required)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['address'].required = False
