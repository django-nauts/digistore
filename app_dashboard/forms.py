from django.core import validators
from django.core.exceptions import ValidationError
from django import forms

from app_account.models import User


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','avatar', 'gender', 'date_of_birth', 'biography']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'cellphone_no': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

        labels = {
            'first_name': 'Firstname',
            'last_name': 'Lastname',
            'avatar': 'Avatar',
            'address': 'Address',
            'date_of_birth': 'Date of birth',
            'cellphone_no': 'Cellphone No.',
            'biography': 'Biography',
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('password and confirm password do not match')

    # def clean_current_password(self):
    #     current_password = self.cleaned_data.get('current_password')
    #     new_password = self.cleaned_data.get('new_password')
    #
    #     if new_password != current_password:
    #         return new_password
    #     raise ValidationError('Your new password should be something different than current password!')

