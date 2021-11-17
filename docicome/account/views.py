from django.shortcuts import render
from django.views import generic

from .forms import AccountCreationForm
from .models import Expertise

def register(request):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form" : form }

    return render(request, 'account/register.html', context)


class ExpertiseView(generic.ListView):
    template_name = 'exp_list.html'
    context_object_name = 'expertise_list'

    def get_queryset(self):
        return Expertise.objects.all()
