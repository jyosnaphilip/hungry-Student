# Generated by Django 4.2.7 on 2024-02-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_orders_options_remove_customer_profile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='Feedback',
            field=models.BooleanField(default=False),
        ),
    ]