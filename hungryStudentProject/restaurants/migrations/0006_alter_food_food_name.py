# Generated by Django 4.2.7 on 2024-01-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_alter_food_food_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='Food_Name',
            field=models.TextField(max_length=25),
        ),
    ]
