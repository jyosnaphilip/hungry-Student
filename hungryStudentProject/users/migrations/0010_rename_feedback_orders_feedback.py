# Generated by Django 4.2.7 on 2024-02-05 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_orders_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='Feedback',
            new_name='feedback',
        ),
    ]