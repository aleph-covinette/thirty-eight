from .models import AudioUploadForm, VideoUploadForm
from django.views import generic
from django.http import HttpResponseRedirect
from .Stream import readMedia, streamQueue

class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('stream-start') != None:
            print("Stream test successful")
            return HttpResponseRedirect('/')
        elif request.GET.get('audio-remove') != None:
            return HttpResponseRedirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audio_list'] = readMedia()
        return context
    
class AudioUploadFormView(generic.FormView):
    form_class = AudioUploadForm
    template_name = 'radio/upload.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class VideoUploadFormView(generic.FormView):
    form_class = VideoUploadForm
    template_name = 'radio/upload.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)