from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("The application page loads properly! Wonderful!")
