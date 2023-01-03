from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import AudioUploadForm
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'
    

class AudioUploadFormView(generic.FormView):
    form_class = AudioUploadForm
    template_name = 'radio/upload.html'
    success_url = '/'