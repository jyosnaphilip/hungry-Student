# Generated by Django 4.2.7 on 2024-01-08 08:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0006_alter_restaurant_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='id',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='rest_id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]