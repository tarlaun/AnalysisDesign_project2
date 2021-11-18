from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from .forms import AccountCreationForm
from django.contrib import messages
from .models import UserType, Doctor, Account, Order, Expertise
from django.views import generic


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


# @login_required
# TODO: If the user isn’t logged in, redirect to settings.LOGIN_URL
# @user_passes_test(being_doctor_check)
def expertise_orders_list(request):
    if not request.user.is_authenticated:
        return HttpResponse("Log in")
    if request.user.user_type == UserType.PATIENT:
        return HttpResponse("You are not a doctor")
    doctor = Doctor.objects.get(user=request.user)
    expertise = doctor.expertise
    orders_list = Order.objects.filter(expertise=expertise, doctor=None)
    return render(request, 'expertise_orders_list.html', {'orders_list': orders_list})


# @login_required
# @user_passes_test(being_doctor_check)
def accept_order(request, order_id):
    if not request.user.is_authenticated:
        return HttpResponse("Log in")
    if request.user.user_type == UserType.PATIENT:
        return HttpResponse("You are not a doctor")
    order = Order.objects.get(id=order_id)
    if order.doctor:
        return HttpResponse("This Order was accepted by another doctor!")
    order.doctor = Doctor.objects.get(user=request.user)
    order.save()
    return render(request, 'accept_order.html', {'order': order})


class ExpertiseView(generic.ListView):
    template_name = 'expertise_list.html'
    context_object_name = 'expertise_list'

    def get_queryset(self):
        return Expertise.objects.all()


def request_for_chosen_expertise(request, exp_id):
    expertise = get_object_or_404(Expertise, pk=exp_id)
    return render(request, 'request_for_expertise.html', {'expertise': expertise})


def add_order(request, exp_id):
    expertise = get_object_or_404(Expertise, pk=exp_id)
    address = request.POST['address']
    details = request.POST['details']
    o = Order(user_id=request.user.id, expertise_id=expertise.id, address=address, details=details)
    o.save()
    return HttpResponseRedirect(reverse('?'))
