from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.index_files, name='index_files'),

]