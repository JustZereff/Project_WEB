from django.urls import path
from . import views

app_name = 'address_book'

urlpatterns = [
    path('', views.index_address_book, name='index_address_book'),
    path('create/', views.create_contact, name='create_contact'),
    path('<int:contact_id>/edit/', views.edit_contact, name='edit_contact'),
    path('<int:contact_id>/', views.contact_detail, name='contact_detail'),  # Добавлено
    path('list/', views.contact_list, name='contact_list'),
]
