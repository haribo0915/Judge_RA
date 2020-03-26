from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'motto']

    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField(required=False)
    motto = forms.CharField(widget=forms.Textarea, required=False)

class SubmissionForm(forms.Form):
    source = forms.CharField(widget=forms.Textarea)