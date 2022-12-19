from django.shortcuts import render
from .forms import LoginForm


def login_page(request):
    form = LoginForm
    return render(request, 'login.html', {
        'form': form,
    })
