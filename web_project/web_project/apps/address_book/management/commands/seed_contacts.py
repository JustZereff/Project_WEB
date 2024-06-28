# Запуск : python manage.py seed_contacts
import random
from datetime import datetime, timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from index.models import Contact
from index.models import CustomUser  # Импортируем вашу модель пользователя

class Command(BaseCommand):
    help = 'Seeds the database with contacts'

    def handle(self, *args, **kwargs):
        fake = Faker('uk_UA')

        # Проверка наличия пользователя с user_id=1
        try:
            user = CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь с ID 1 не найден'))
            return

        for _ in range(50):  # Создаем 50 контактов
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone = fake.phone_number()[:15]  # Ограничиваем длину телефонного номера до 15 символов
            address = fake.address()
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)

            # Создаем и сохраняем новый контакт
            Contact.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                birth_date=birth_date,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        self.stdout.write(self.style.SUCCESS('База данных заполнена фейк-контактами'))
