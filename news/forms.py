from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.utils import timezone
from django.conf import settings


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "url"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class EditComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def clean(self):
        cleaned_data = super().clean()
        comment = self.instance
        time_difference = timezone.now() - comment.pubDate
        if time_difference.total_seconds() > settings.ALLOWED_EDIT_SECONDS:
            minutes_allowed = round(settings.ALLOWED_EDIT_SECONDS / 60)
            raise forms.ValidationError(
                f"Comment can only be edited within {minutes_allowed} minutes"
            )
        return cleaned_data
