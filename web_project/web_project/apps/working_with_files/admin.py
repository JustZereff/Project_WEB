from django.contrib import admin
from .models import File
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category', 'uploaded_at']

    def get_category(self, obj):
        return obj.get_category()
    get_category.short_description = 'Категорія'