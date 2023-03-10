from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.FileUploadFormView.as_view(), name='upload'),
    path('config/', views.ConfigurationEditView.as_view(), name='config')
]