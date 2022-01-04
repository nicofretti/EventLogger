from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import api.models as models
import json

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
    loggers = models.LoggerKey.objects.all()
    for logger in loggers:
        if(models.Event.objects.filter(logger_key=logger.id).exists()):
            logger.last_event = models.Event.objects.filter(logger_key=logger.id).latest('timestamp').timestamp
        else:
            logger.last_event = "-"
    return render(request, 'homepage.html', {'loggers': loggers})

def events(request,pk):
    events = models.Event.objects.filter(logger_key=pk)
    custom_events = []
    for event in events:
        processes = json.loads(event.processes)
        print(processes)
        event.processes = processes
        custom_events.append(event)
    context = {
        'events': custom_events,
        'logger': models.LoggerKey.objects.get(id=pk)
    }
    return render(request,'events.html', context)
