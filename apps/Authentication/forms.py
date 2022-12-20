from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    task_id = forms.CharField(
        label='Task ID',
        max_length=100,
    )
    password = forms.CharField(widget=forms.PasswordInput())
