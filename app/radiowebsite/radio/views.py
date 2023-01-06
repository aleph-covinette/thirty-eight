import os
from threading import Thread
from django.views import generic
from django.http import HttpResponseRedirect
from .models import FileUploadForm, FileUpload, ConfigurationForm, Configuration
from .Stream import streamQueue, getDuration


class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('stream-start') != None:
            streamconfig = Configuration.objects.get()
            aqueue = [(i.file.name, i.duration) for i in FileUpload.objects.filter(filetype='audio')]
            vqueue = [(i.file.name, i.duration) for i in FileUpload.objects.filter(filetype='video')]
            nstream = Thread(target=streamQueue, args=(aqueue, vqueue, streamconfig.streamkey,))
            nstream.start()
            return HttpResponseRedirect('/')
        elif request.GET.get('file-remove') != None:
            target = list(request.GET)[0]
            target_file = FileUpload.objects.filter(id=target).get().file.name
            try:
                os.remove(os.getcwd() + '/media/' + target_file)
            except FileNotFoundError:
                pass
            FileUpload.objects.filter(id=target).delete()
            return HttpResponseRedirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audio_list'] = FileUpload.objects.filter(filetype='audio')
        context['video_list'] = FileUpload.objects.filter(filetype='video')
        return context


class FileUploadFormView(generic.FormView):
    form_class = FileUploadForm
    template_name = 'radio/upload.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        target = FileUpload.objects.filter(duration=-1).get()
        target.duration = getDuration(target.file.name)
        target.save()
        return super().form_valid(form)


class ConfigurationEditView(generic.FormView):
    form_class = ConfigurationForm
    template_name = 'radio/config.html'
    success_url = '/'

    def form_valid(self, form):
        Configuration.objects.all().delete()
        form.save()
        return super().form_valid(form)
