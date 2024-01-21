from django.db import models
import uuid
from customadmin.models import Restaurant

# Create your models here.

# model for restaurant menu

class Food(models.Model):
    Food_ID=models.UUIDField(primary_key=True,auto_created=True,default=uuid.uuid4,help_text='unique ID for each food across all models')
    Food_Name=models.TextField(max_length=25,blank=False,unique=True,error_messages={'unique': ("A user with that email address already exists."),
    })
    CATEGORIES=(
        ('starter','Starter'),
        ('main_course','Main Course'),
        ('dessert','Desserts'),
        ('beverage','Beverages'),
        )
    Category=models.CharField(max_length=50,choices=CATEGORIES,blank=True,null=True,default='main_course')
    Image=models.ImageField(upload_to='food_images/')
    Description=models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        ordering=['Food_Name']
    def __str__(self):
         #String for representing the Model object.
        return f'{self.Food_Name}'
    
    



class Restaurant_Food_bridge(models.Model):
    rest_id=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Food_ID=models.ForeignKey(Food,on_delete=models.CASCADE)
    Status=models.BooleanField(blank=False,default=True)
    Price=models.DecimalField(max_digits=5,decimal_places=2,blank=False)

    def __str__(self):
        return str(self.rest_id.__str__()) +" - "+str(self.Food_ID.__str__())
    