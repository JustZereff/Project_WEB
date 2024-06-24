from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

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
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    address = models.TextField(_('address'), blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)  # Новое поле
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.user.email})'
    
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


# class File(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')
#     name = models.CharField(_('file name'), max_length=255)
#     file = CloudinaryField(_('file'))
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     updated_at = models.DateTimeField(_('updated at'), auto_now=True)

#     def __str__(self):
#         return f'{self.name} ({self.user.email})'
