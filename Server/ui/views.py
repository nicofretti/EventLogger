from django.shortcuts import render
from django.contrib.auth import authenticate, login


# Create your views here.
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Logged
        pass
    else:
        # Invalid login
        pass
