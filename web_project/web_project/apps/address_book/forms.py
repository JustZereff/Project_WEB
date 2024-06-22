from django import forms
from web_project.apps.index.models import Contact  # Использование абсолютного пути
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address', 'birth_date']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise forms.ValidationError('Введите корректный email адрес.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError('Введите корректный номер телефона. До 15 цифр допустимо.')
        return phone
