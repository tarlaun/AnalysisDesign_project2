from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .forms import AccountCreationForm


def being_doctor_check(user):
    return user.user_type == 2


def register(request):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}

    return render(request, 'account/register.html', context)


def login(request):
    form = AccountCreationForm()
    context = {"form": form}
    return render(request, 'account/login.html', context)
