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
    # Пока что не нужно
    protocol = models.BooleanField()
