from django.contrib import admin
from index.models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'uploaded_at']
    search_fields = ['name', 'user__email']

    def get_category(self, obj):
        return obj.get_category_display()
    get_category.short_description = 'Категорія'
