from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, UserType

# class AccountCreationForm(UserCreationForm):
#     class Meta:
#         model = Account
#         fields = Account.get_form_fields()

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account        
        fields = Account.get_form_fields()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )

    class Meta:
        model = Account
        fields = (
            "username",
            "password",
        )