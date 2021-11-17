from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from .forms import AccountCreationForm
from .models import Expertise, Order
from django.views import generic


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
