import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import api.models as models
import json
import random


def login(request):
    template = "login.html"
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # Logged
            auth_login(request, user)
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
def settings(request, pk):
    logger = models.LoggerKey.objects.get(id=pk)
    settings = json.loads(logger.settings)
    context = {
        'logger': logger,
        'settings': settings
    }
    return render(request, 'settings.html', context)

@login_required(login_url='login/')
def homepage(request):
    loggers = models.LoggerKey.objects.all()
    for logger in loggers:
        if (models.Event.objects.filter(logger_key=logger.id).exists()):
            logger.last_event = models.Event.objects.filter(logger_key=logger.id).latest('timestamp').timestamp
        else:
            logger.last_event = "-"
    return render(request, 'homepage.html', {'loggers': loggers})


@login_required(login_url='login/')
def events(request, pk):
    # if request has start and end date filter events
    context = {}
    if request.GET.get('start') and request.GET.get('end'):
        start = request.GET.get('start')
        end = request.GET.get('end')
        events = models.Event.objects.filter(logger_key=pk, timestamp__gte=start, timestamp__lte=end)
        context['start'] = start
        context['end'] = end
    else:
        events = models.Event.objects.filter(logger_key=pk)

    if request.GET.get('q'):
        q = request.GET.get('q')
        events = events.filter(content__contains=request.GET.get('q'))
        context['q'] = q
    assigned_colors = {}
    custom_events = []
    for event in events:
        processes = json.loads(event.processes)
        processes_string, assigned_colors = get_processes_to_string(processes, assigned_colors)
        event.processes = processes_string
        custom_events.append(event)
    paginator = Paginator(custom_events, 15)
    page = request.GET.get('page')
    context['page_obj'] = paginator.get_page(page)
    context['logger'] = models.LoggerKey.objects.get(id=pk)

    return render(request, 'events.html', context)

@login_required(login_url='login/')
def charts(request, pk):
    logger = models.LoggerKey.objects.get(id=pk)
    print("fuck you")
    return render(request, 'charts.html', {"logger":logger})

# Useful methods

def get_processes_to_string(processes, assigned_colors):
    processes_custom = []
    for obj in processes:
        list_processes = ""
        for p in obj['list']:
            if (p in assigned_colors):
                color = assigned_colors[p]
            else:
                random.shuffle(rainbow_colors)
                color = rainbow_colors[random.randint(0, len(rainbow_colors) - 1)]
                assigned_colors[p] = color
            list_processes += """<span class='process'><span style='color:{}'>●</span>{}</span> """.format(color, p)
        obj['timestamp'] = datetime.datetime \
            .strptime(obj['timestamp'], '%d/%m/%Y %H:%M:%S') \
            .strftime('%H:%M:%S')
        obj['list'] = list_processes.strip(',')
        processes_custom.append(obj)
    return processes_custom, assigned_colors


rainbow_colors = [
    '#ff0000', '#ffa500', '#ffff00', '#008000', '#0000ff', '#800080', '#808080', '#a52a2a', '#ffc0cb', '#00ffff',
    '#ff00ff', '#dc143c', '#4b0082', '#00ff00', '#808000', '#008080', '#000080', '#800000', '#c0c0c0', '#32cd32',
    '#ffd700', '#fa8072 '
]
