from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name *'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email *'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Comment *'}),
        }
