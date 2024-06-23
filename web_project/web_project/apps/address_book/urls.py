# addressbook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_address_book, name='index_address_book'),
    path('contact/create/', views.create_contact, name='create_contact'),
    path('contact/<int:pk>/update/', views.update_contact, name='update_contact'),
    path('contact/<int:pk>/delete/', views.delete_contact, name='delete_contact'),
    path('contact/<int:pk>/', views.view_contact, name='view_contact'),
]
