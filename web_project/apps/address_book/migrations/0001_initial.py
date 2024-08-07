# Generated by Django 5.0.6 on 2024-06-22 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='phone number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
        ),
    ]
