from django.db import models
import os

class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Зображення'),
        ('document', 'Документ'),
        ('video', 'Відео'),
        ('other', 'Інше'),
    ]

    name = models.CharField(max_length=255, verbose_name="Назва")
    file = models.FileField(upload_to='uploads/', verbose_name="Файл")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other', verbose_name="Категорія")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата завантаження")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.category or self.category == 'other':
            self.category = self._determine_category()
        super().save(*args, **kwargs)

    def _determine_category(self):
        extension = os.path.splitext(self.file.name)[1].lower()
        if extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            return 'image'
        elif extension in ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf']:
            return 'document'
        elif extension in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            return 'video'
        else:
            return 'other'
