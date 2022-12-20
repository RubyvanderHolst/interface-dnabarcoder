from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm
from apps.Authentication.models import TaskInfo


def login_page(request):
    # View function for log in page and authentication for log in
    error_message = ''
    if request.method == 'POST':
        task_id = request.POST['task_id']
        password = request.POST['password']
        user = authenticate(username=task_id, password=password)
        # if user (a.k.a. task_id) exists in database
        if user is not None:
            login(request, user)
            db_entry = TaskInfo.objects.get(user__username=task_id)
            results_url = db_entry.get_absolute_url()
            return redirect(results_url)
        else:
            error_message = 'Could not log in with given credentials'
    form = LoginForm
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message,
    })
