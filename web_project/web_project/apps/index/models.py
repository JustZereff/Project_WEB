from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)  # Новое поле
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(_('first_name'), max_length=100, null=True)
    last_name = models.CharField(_('last_name'), max_length=100, null=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    address = models.CharField(_('address'), max_length=150, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)  # Новое поле
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.user.email})'
    
    def days_until_birthday(self):
        from datetime import date
        today = date.today()
        if self.birth_date:
            next_birthday = self.birth_date.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

class Tag(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.user.email})'

    def add_tags(self, tag_names):
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        self.tags.set(tags)

User = get_user_model()

class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Зображення'),
        ('document', 'Документи'),
        ('video', 'Відео'),
        ('other', 'Інше'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
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
