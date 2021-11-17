from django.shortcuts import render

from .forms import AccountCreationForm


def register(request):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}

    return render(request, 'account/register.html', context)


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


def accept_order(request, order_id):
    # if is doctor and same expertise and order is not taken by others
    order = {'id': 1, 'patient': {'name': 'نام بیمار اول'},
           'address': 'آدرس ۱', 'problem': 'شرح ۱'}
    return render(request, 'accept_order.html', {'order': order})
