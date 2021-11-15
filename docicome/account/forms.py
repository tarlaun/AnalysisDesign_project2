from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import fields_for_model
from .models import Account, UserType

class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('username', 'email','first_name', 'last_name')

