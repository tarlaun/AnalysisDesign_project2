from django.shortcuts import render

from .forms import AccountCreationForm

def register(request):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form" : form }

    return render(request, 'account/register.html', context)
