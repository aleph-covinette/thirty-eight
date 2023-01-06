import os
from .models import FileUploadForm, FileUpload, ConfigurationForm, Configuration
from django.views import generic
from django.http import HttpResponseRedirect

class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('stream-start') != None:
            streamconfigs = Configuration.objects.all()
            for i in streamconfigs:
                print('[XIV] Обнаружена конфигурация стрима, ключ: ' + i.streamkey)
            return HttpResponseRedirect('/')
        elif request.GET.get('audio-remove') != None:
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
        context['audio_list'] = FileUpload.objects.all()
        return context
    
class FileUploadFormView(generic.FormView):
    form_class = FileUploadForm
    template_name = 'radio/upload.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ConfigurationEditView(generic.FormView):
    form_class = ConfigurationForm
    template_name = 'radio/config.html'
    success_url = '/'

    def form_valid(self, form):
        Configuration.objects.all().delete()
        form.save()
        return super().form_valid(form)