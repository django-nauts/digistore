from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'singin-email-2',
        }),
        validators=[validators.EmailValidator, validators.MaxLengthValidator(100)],
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'singin-password-2',
        }),
        validators=[validators.MaxLengthValidator(100)],
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        validators=[validators.EmailValidator, validators.MaxLengthValidator(100)],
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        validators=[validators.MinLengthValidator(5), validators.MaxLengthValidator(100)],
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'singin-password-2',
        }),
        validators=[validators.MaxLengthValidator(100)],
    )
    confirm_password = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'singin-password-2',
        }),
        validators=[validators.MaxLengthValidator(100)],
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('Password and confirm password do not match')


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'singin-email-2',
        }),
        validators=[validators.EmailValidator, validators.MaxLengthValidator(100)],
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'singin-password-2',
        }),
        validators=[validators.MaxLengthValidator(100)],
    )
    confirm_password = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'singin-password-2',
        }),
        validators=[validators.MaxLengthValidator(100)],
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('Password and confirm password do not match')
