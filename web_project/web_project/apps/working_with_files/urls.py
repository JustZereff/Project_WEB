from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.index_files, name='index_files'),
    path('delete/<int:pk>/', views.file_delete, name='file_delete'),
    path('upload/', views.file_upload, name='file_upload'),


]