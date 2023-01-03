from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('audio/', views.AudioUploadFormView.as_view(), name='audio'),
    path('video/', views.VideoUploadFormView.as_view(), name='video')
]