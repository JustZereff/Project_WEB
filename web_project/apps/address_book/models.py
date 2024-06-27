from django.db import models
from django.utils.translation import gettext_lazy as _


# class Contact(models.Model):
#     name = models.CharField(_('name'), max_length=100)
#     email = models.EmailField(_('email address'), blank=True, null=True)
#     phone = models.CharField(
#         _('phone number'), max_length=15, blank=True, null=True)
#     address = models.TextField(_('address'), blank=True, null=True)
#     birth_date = models.DateField(_('birth date'), blank=True, null=True)
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     updated_at = models.DateTimeField(_('updated at'), auto_now=True)

#     def __str__(self):
#         return self.name
