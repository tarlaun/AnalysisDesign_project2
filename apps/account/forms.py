from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, UserType, DEGREE_TYPES, Expertise
from django.core.validators import MaxValueValidator, MinValueValidator


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = Account.get_form_fields()

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

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        )
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        )
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Phone Number (+9999999999)", "class": "form-control"}
        )
    )
    user_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        choices=UserType.choices,
        label="User Type",
    )
    degree_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        choices=DEGREE_TYPES.choices,
        label="Degree",
    )
    work_experience = forms.IntegerField(
        required=True,
        min_value=0, 
        max_value=100,
        widget=forms.NumberInput(
            attrs={"placeholder": "Work Experiance (in years)", "class": "form-control"}
        )
    )
    expertise_list = [(i+1, e.name) for i, e in enumerate(Expertise.objects.all())]
    expertises = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        choices=expertise_list,
        label="Expertises",
    )

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "phone_number",
            "user_type",
            "degree_type",
            "work_experience",
            "expertises"
        )