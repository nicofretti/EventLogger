from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout


def login(request):
    template = "authentication/login.html"
    user = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Logged
            return HttpResponseRedirect('/')
        else:
            # Invalid login
            return render(request, template, {'error': 'Invalid login'})
    return render(request, template)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('login')


def homepage(request):
    return render(request, 'homepage.html')
