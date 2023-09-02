from accounts.models import User
from django import forms


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "age", "address")