from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.index_address_book, name='index_address_book'),

]