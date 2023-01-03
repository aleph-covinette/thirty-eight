from django.db import models
from django.forms import ModelForm

class AudioUpload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='audio/')

class AudioUploadForm(ModelForm):
    class Meta():
        model = AudioUpload
        fields = '__all__'