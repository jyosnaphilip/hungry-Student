from django.db import models
import uuid

# Create your models here.

# model for restaurant menu

class Food(models.Model):
    Food_id=models.UUIDField(auto_created=True,primary_key=True,default=uuid.uuid)
    Food_Name=models.TextField(max_length=25,blank=)
    Category=models.TextChoices()

    Image=models.ImageField()

class Restaurant_Food_bridge(models.Model):
