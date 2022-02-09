import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
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
    # start is in datetime-local format YYYY-MM-DDThh:mm
    start = datetime.datetime.now().strftime("%Y-%m-%d")
    context = {
        'logger': logger,
        'start': "2022-01-09"
    }
    return render(request, 'charts.html', context)


@login_required(login_url='login/')
def chart_ajax(request, pk):
    logger = models.LoggerKey.objects.get(id=pk)
    start = request.GET.get('start')
    if (start):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = request.GET.get('end')
    chart = request.GET.get('chart')
    data = {}
    events = models.Event.objects.filter(logger_key=logger.id, timestamp__gte=start,
                                         timestamp__lte=start + datetime.timedelta(days=1))
    if chart == '1':
        # Total usage for each app/process
        usage = {}
        previous_timestamp = None  # used to calculate the time between two events format 01/09/2022 01:00:00
        for event in events:
            processes = json.loads(event.processes)
            for process in processes:
                timestamp = datetime.datetime.strptime(process['timestamp'], "%d/%m/%Y %H:%M:%S")
                if previous_timestamp:
                    time_diff = timestamp - previous_timestamp
                    if time_diff.seconds <= 60:
                        # more than one minute maybe the logger is not working
                        for app in process['list']:
                            if app in usage:
                                usage[app] += time_diff.seconds
                            else:
                                usage[app] = time_diff.seconds
                previous_timestamp = timestamp
        categories = usage.keys()
        data['categories'] = [category.capitalize() for category in categories]
        data['series'] = [round(usage[category] / 60) + 1 for category in categories]

    if chart == '2':
        # Total events per day order by time

        counter = {}
        previous = start - datetime.timedelta(minutes=30)
        max_events = -1
        argmax = -1
        for _ in range(48):
            counter[start] = 0
            subset = events.filter(timestamp__gte=previous, timestamp__lte=start)
            for event in subset:
                counter[start] += int(event.content.count('kbd') / 2)
                counter[start] += event.content.count('class')
                if counter[start] > max_events:
                    max_events = counter[start]
                    argmax = start
            previous = start
            start += datetime.timedelta(minutes=30)
        data['categories'] = [start.strftime("%H:%M") for start in counter.keys()]
        data['series'] = [counter[start] for start in counter.keys()]
        data['zoom'] = [(list(counter.keys()).index(argmax) - 3) % 48, (list(counter.keys()).index(argmax) + 3) % 48]

    if chart == '3':
        # App usage per day order by time
        apps = {}  # {app:  [[time1,time3],[time2,time4]...]} final result
        last_interval = {}  # {app: [start,stop]} used to calculate the time between two events of the same app
        for event in events:
            processes = json.loads(event.processes)
            for process in processes:
                timestamp = datetime.datetime.strptime(process['timestamp'], "%d/%m/%Y %H:%M:%S")
                for app in process['list']:
                    if app in apps:
                        time_diff = timestamp - last_interval[app][1]
                        if time_diff.seconds > 60 * 5:
                            # different time interval
                            apps[app].append(last_interval[app])
                            last_interval[app] = [timestamp, timestamp]
                        else:
                            # update last timestamp
                            last_interval[app][1] = timestamp
                    else:
                        # add app in apps dict
                        apps[app] = []
                        # todo: better 30 seconds
                        last_interval[app] = [timestamp, timestamp + datetime.timedelta(seconds=30)]
        # attach the last interval
        for app in last_interval:
            if last_interval[app][1] != last_interval[app][0]:
                apps[app].append(last_interval[app])
        data = {'list': []}
        for app in apps:
            random.shuffle(rainbow_colors)
            color = rainbow_colors[random.randint(0, len(rainbow_colors) - 1)]
            appname = app.capitalize()
            for interval in apps[app]:
                data['list'].append({'x': appname, 'y': interval, 'fillColor': color})
    return JsonResponse(data)


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


rainbow_colors = ["#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0", "#FFFF00", "#FF00FF", "#00FFFF" , "#FFC0CB", "#C0C0C0"]

# rainbow_colors = [
#    '#ff0000', '#ffa500', '#ffff00', '#008000', '#0000ff', '#800080', '#808080', '#a52a2a', '#ffc0cb', '#00ffff',
#    '#ff00ff', '#dc143c', '#4b0082', '#00ff00', '#808000', '#008080', '#000080', '#800000', '#c0c0c0', '#32cd32',
#    '#ffd700', '#fa8072 '
# ]
