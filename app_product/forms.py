from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)

    class Meta:
        model = Comment
        fields = ("comment", "author", "rating")
