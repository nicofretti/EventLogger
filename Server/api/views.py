import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

import api.models as models


def get_processes(raw_data):
    # format: get all processes inside a string that are in the format of "<process_name,...,process_name>...<...>"
    # return a list of all subsets of processes
    array = []
    processes_list = re.findall(r'<(.*?)>', raw_data)
    for processes in processes_list:
        array.append(processes.split(','))
    return array


def translate_key(key):
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
    return "<kbd>{}</kbd>".format(key)


def get_content(raw_data):
    # format: string that contains all events logged "asdasdasd<process_name,...>[key]..."
    # return string where all key are replaced with value
    key_to_replace = re.findall(r'\[(.*?)\]', raw_data)
    for key in key_to_replace:
        raw_data = raw_data.replace("["+key+"]", translate_key(key))
        print(key,translate_key(key),raw_data)
    return raw_data


@csrf_exempt
def log(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    # Request data are in json format
    data = json.load(request)
    lines = data['content'].split(' $ ')
    for line in lines:
        time, raw_data = line.split(' | ')
        processes = get_processes(raw_data)
        content = get_content(raw_data)
        print(content)
        # event = models.Event.objects.create(
        #    key=data['key'],
        #    timestamp=time,
        #    content=content,
        #    processes=json.dumps(processes)
        # )
    return HttpResponse(status=200)
