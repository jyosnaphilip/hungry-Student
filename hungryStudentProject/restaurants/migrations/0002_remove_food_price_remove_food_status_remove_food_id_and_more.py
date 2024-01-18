# Generated by Django 4.2.7 on 2024-01-07 19:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='Price',
        ),
        migrations.RemoveField(
            model_name='food',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='food',
            name='id',
        ),
        migrations.AlterField(
            model_name='food',
            name='Food_ID',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, help_text='unique ID for each food across all models', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='food',
            name='Image',
            field=models.ImageField(upload_to='food_images/'),
        ),
        migrations.CreateModel(
            name='Restaurant_Food_bridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.BooleanField(default=True)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Food_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.food')),
            ],
        ),
    ]