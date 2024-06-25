from django import forms
from index.models import Contact
from django.core.validators import EmailValidator


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'birth_date']
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'phone': "Телефон",
            'address': 'Адреса',
            'birth_date': 'Дата народження'
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Пример простой валидации телефона (можно настроить под конкретные требования)
        if not phone.isdigit():
            raise forms.ValidationError('Номер телефону повинен складатися лише з цифр.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Простая валидация email с использованием встроенного валидатора
        validator = EmailValidator('Введіть коректний email.')
        validator(email)
        return email
