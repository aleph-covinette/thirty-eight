from django.db import models
from django.forms import ModelForm
from random import randint 

class FileUpload(models.Model):
    def getFiletype(instance, filename):
        return '/'.join([instance.filetype, filename])
    title = models.CharField(max_length=50)
    AUDIO = 'audio'
    VIDEO = 'video'
    filetypes = [
        (AUDIO, 'Музыка'),
        (VIDEO, 'Видео')
    ]
    filetype = models.CharField(choices=filetypes, default=AUDIO, max_length=10)
    file = models.FileField(upload_to=getFiletype)

class FileUploadForm(ModelForm):
    class Meta():
        model = FileUpload
        fields = ['title', 'filetype', 'file']

class Configuration(models.Model):
    protocol = models.BooleanField()
