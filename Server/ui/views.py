from django.shortcuts import render
from django.contrib.auth import authenticate, login


def login(request):
    template = "authentication/login.html"
    user = None
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

    if user is not None:
        # Logged
        pass
    else:
        # Invalid login
        pass
    return render(request,template,{})
