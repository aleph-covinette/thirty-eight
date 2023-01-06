from django.db import models
from django.forms import ModelForm

class FileUpload(models.Model):
    def getFiletype(instance, filename):
        return '/'.join([instance.filetype, filename])
    title = models.CharField(max_length=50, verbose_name='Название')
    AUDIO = 'audio'
    VIDEO = 'video'
    filetypes = [
        (AUDIO, 'Музыка'),
        (VIDEO, 'Видео')
    ]
    filetype = models.CharField(choices=filetypes, default=AUDIO, max_length=10, verbose_name='Тип файла')
    file = models.FileField(upload_to=getFiletype, verbose_name='Файл')

class FileUploadForm(ModelForm):
    class Meta():
        model = FileUpload
        fields = '__all__'

class Configuration(models.Model):
    RTMP = 'yt_rtmp'
    protocols = [
        (RTMP, 'RTMP (YouTube)')
    ]
    protocol = models.CharField(choices=protocols, default=RTMP, max_length=10, verbose_name='Протокол')
    streamkey = models.CharField(max_length=24, default='xxxx-xxxx-xxxx-xxxx-xxxx', verbose_name='Ключ стрима')

class ConfigurationForm(ModelForm):
    class Meta():
        model = Configuration
        fields = '__all__'