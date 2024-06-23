from django.contrib import admin
from .models import CustomUser, Contact, Note, Tag

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'user', 'created_at')
    search_fields = ('name', 'email', 'phone', 'user__email')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__email')
    filter_horizontal = ('tags',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

# @admin.register(File)
# class FileAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at')
#     search_fields = ('name', 'user__email')
