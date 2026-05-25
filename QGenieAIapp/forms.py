from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UploadedFile

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.
    Extends Django's default UserCreationForm to include email and proper styling.
    """
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark-input text-white border-secondary'
            field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'


class UserLoginForm(AuthenticationForm):
    """
    Form for user login.
    Extends Django's AuthenticationForm and adds custom styling.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark-input text-white border-secondary',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark-input text-white border-secondary',
        'placeholder': 'Enter your password'
    }))


class UploadedFileForm(forms.ModelForm):
    """
    Form to upload files.
    Restricts input to PDF and TXT file fields with styling.
    """
    class Meta:
        model = UploadedFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'form-control bg-dark-input text-white border-secondary',
            'accept': '.pdf,.txt',
        })


class OTPVerificationForm(forms.Form):
    """
    Form for validating the OTP verification code.
    """
    otp_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark-input text-white border-secondary text-center fs-4 fw-bold',
            'placeholder': '123456',
            'autocomplete': 'off',
            'style': 'letter-spacing: 0.5rem;',
        }),
        label="OTP Verification Code"
    )

    def clean_otp_code(self):
        otp_code = "".join(self.cleaned_data.get('otp_code', '').split())
        if not otp_code.isdigit():
            raise forms.ValidationError("OTP code must contain digits only.")
        return otp_code


from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    """
    Form to update user core fields.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark-input text-white border-secondary'
            label = field.label or field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = f'Enter {label.lower()}'


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form to update user profile specific fields.
    """
    class Meta:
        model = UserProfile
        fields = ['avatar', 'theme', 'theme_mode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control bg-dark-input text-white border-secondary',
            'accept': 'image/*',
        })
        self.fields['theme'].widget.attrs.update({
            'class': 'form-select bg-dark-input text-white border-secondary',
        })
        self.fields['theme_mode'].widget.attrs.update({
            'class': 'form-select bg-dark-input text-white border-secondary',
        })


