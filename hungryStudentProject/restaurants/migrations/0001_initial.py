# Generated by Django 4.2.7 on 2024-01-04 19:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Food_ID', models.UUIDField(auto_created=True, default=uuid.uuid4, help_text='unique ID for each food across all models')),
                ('Food_Name', models.TextField(max_length=25)),
                ('Category', models.CharField(blank=True, choices=[('starter', 'Starter'), ('main_course', 'Main Course'), ('dessert', 'Desserts'), ('beverage', 'Beverages')], default='main_course', max_length=50, null=True)),
                ('Image', models.ImageField(upload_to='')),
                ('Status', models.CharField(choices=[('A', 'Available'), ('NA', 'Not Available')], default='A', max_length=2)),
                ('Price', models.IntegerField()),
            ],
            options={
                'ordering': ['Food_Name'],
            },
        ),
    ]
