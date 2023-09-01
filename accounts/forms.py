from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("first_name", "lastname", "age", "email", "address")

class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ("first_name", "last_name", "age", "email", "address")