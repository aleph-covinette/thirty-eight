from django.db import models
from django.forms import ModelForm

class AudioUpload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='audio/')

class VideoUpload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='video/')

class AudioUploadForm(ModelForm):
    class Meta():
        model = AudioUpload
        fields = '__all__'

class VideoUploadForm(ModelForm):
    class Meta():
        model = VideoUpload
        fields = '__all__'