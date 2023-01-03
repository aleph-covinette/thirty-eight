from .models import AudioUploadForm
from django.views import generic
from .Stream import readMedia

class IndexView(generic.TemplateView):
    template_name = 'radio/index.html'
    
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
