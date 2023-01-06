import os
import subprocess
from threading import Thread
from .models import FileUploadForm, FileUpload, ConfigurationForm, Configuration
from .Stream import streamQueue
from django.views import generic
from django.http import HttpResponseRedirect

class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('stream-start') != None:
            streamconfigs = Configuration.objects.all()
            key = streamconfigs[0].streamkey
            aqueue = [(i.file.name, i.duration) for i in FileUpload.objects.filter(filetype='audio')]
            vqueue = [(i.file.name, i.duration) for i in FileUpload.objects.filter(filetype='video')]
            nstream = Thread(target=streamQueue, args=(aqueue, vqueue, key,))
            nstream.start()
            return HttpResponseRedirect('/')
        elif request.GET.get('file-remove') != None:
            target = list(request.GET)[0]
            target_file = FileUpload.objects.filter(id=target)[0].file.name
            try:
                os.remove(os.getcwd() + '/media/' + target_file)
            except FileNotFoundError:
                print('[XIV] Внимание! Обнаружена аномалия файловой системы. Если вы удаляли файлы вручную - больше так не делайте.')
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
        target = FileUpload.objects.filter(flength=-1).get()
        popen = subprocess.Popen(
        ("ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-i", 'media/' + target.file.name),
        stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        output = str(output)
        output = output[output.find("duration") + len("duration") + 1: output.rfind("FORMAT") - 6]
        target.duration = int(round(float(output) + 0.5))
        print('[XIV] Target length calculated:', target.duration)
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