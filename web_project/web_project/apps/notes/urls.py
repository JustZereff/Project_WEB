from django.urls import path, reverse_lazy
from . import views


# app_name = 'notes'

urlpatterns = [
    path('', views.index_notes, name='index_notes'),
    path('create/', views.create_note, name='create_note'),
    path('tag/create/', views.create_tag, name='create_tag'),
    path('tag/<str:tag_name>/', views.sort_notes_by_tag, name='sort_notes_by_tag'),
    path('note/<int:note_id>/', views.view_note, name='view_note'),
    path('note/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('note/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('sort/', views.sort_notes_by_date, name='sort_notes_by_date')
]