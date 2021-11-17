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


@login_required
# TODO: If the user isn’t logged in, redirect to settings.LOGIN_URL
@user_passes_test(being_doctor_check)
def expertise_orders_list(request):
    # doctor = request.auth.doctor
    # expertise = doctor.expertise
    # orders_list = filter(orders.all, expertise=expertise)
    orders_list = [
        {'id': 1, 'patient': {'name': 'نام بیمار اول'},
         'address': 'آدرس ۱', 'problem': 'شرح ۱'},
        {'id': 2, 'patient': {'name': 'نام بیمار دوم'},
         'address': 'آدرس ۲', 'problem': 'شرح ۲'},
        {'id': 3, 'patient': {'name': 'نام بیمار سوم'},
         'address': 'آدرس ۳', 'problem': 'شرح ۳'},
    ]
    return render(request, 'expertise_orders_list.html', {'orders_list': orders_list})


@login_required
@user_passes_test(being_doctor_check)
def accept_order(request, order_id):
    print(request.user.is_authenticated)
    # if is doctor and same expertise and order is not taken by others
    order = {'id': 1, 'patient': {'name': 'نام بیمار اول'},
             'address': 'آدرس ۱', 'problem': 'شرح ۱'}
    return render(request, 'accept_order.html', {'order': order})
