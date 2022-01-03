from django.http import HttpResponse
from django.shortcuts import render
import api.models as models

# Create your views here.
def log(request):
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")
    return HttpResponse("Hello, world. You're at the polls index.")