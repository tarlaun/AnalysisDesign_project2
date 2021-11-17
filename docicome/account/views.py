from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import AccountCreationForm
from django.contrib import messages


def being_doctor_check(user):
    return user.user_type == 2


def register(request):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            # TODO error
            pass

    context = {"form": form}

    return render(request, 'account/register.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password is incorrect. <a href="">Return to login</a>')

    form = AccountCreationForm()
    context = {"form": form}
    return render(request, 'account/login.html', context)


def logout(request):
    logout(re)


def home(request):
    return HttpResponse("Home Page")