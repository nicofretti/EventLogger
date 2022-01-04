import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

import api.models as models
def get_processes(str):
    # format: get all processes inside a string that are in the format of "<process_name,...,process_name>...<...>"
    # return a list of all subsets of processes
    array = []
    for processes in re.findall(r'<(.*?)>', str):
        array.append(processes.split(','))
    return array

@csrf_exempt
def log(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    # Request data are in json format
    data = json.load(request)
    key = data['key']
    lines = data['content'].split(' $ ')
    for line in lines:
        time, content = line.split(' | ')
        processes = get_processes(content)
        print(time, processes)
    return HttpResponse(status=200)
