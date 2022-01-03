from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login(request):
    template = "login.html"
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # Logged
            auth_login(request,user)
            return HttpResponseRedirect('/')
        else:
            # Invalid login
            return render(request, template, {'error': 'Invalid login'})
    return render(request, template)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('login')


@login_required(login_url='login/')
def homepage(request):
    return render(request, 'homepage.html')
