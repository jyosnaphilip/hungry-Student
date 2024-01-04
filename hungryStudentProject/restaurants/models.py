from django.db import models
import uuid

# Create your models here.

# model for restaurant menu

class Food(models.Model):
    Food_ID=models.UUIDField(auto_created=True,default=uuid.uuid4,help_text='unique ID for each food across all models')
    # Restaurant_ID=models.ForeignKey('Restaurants',max_length=200,on_delete=models.SET_NULL,Null=True,blank=False)
    Food_Name=models.TextField(max_length=25,blank=False)
    CATEGORIES=(
        ('starter','Starter'),
        ('main_course','Main Course'),
        ('dessert','Desserts'),
        ('beverage','Beverages'),
        )
    Category=models.CharField(max_length=50,choices=CATEGORIES,blank=True,null=True,default='main_course')
    Image=models.ImageField()
    Status_Val=(
        ('A','Available'),
        ('NA','Not Available'),
    )
    Status=models.CharField(max_length=2,choices=Status_Val,blank=False,default='A')
    Price=models.IntegerField(blank=False)


    class Meta:
        ordering=['Food_Name']
    
    # def __str__(self):
    #      #String for representing the Model object.
    #     return f'{self.Food_ID} ({self.Food_Name})'
    



# class Restaurant_Food_bridge(models.Model):
#     Restaurant_ID=models.ForeignKey('Restaurant',on_delete=models.SET_NULL,Null='True')
#     Food_ID=models.ForeignKey('Food',on_delete=models.SET_NULL,Null='True')
#     Status_Val=(
#         ('Available'),('NA')
#     )
#     Status=models.CharField(max_length=10,choices=Status_Val,blank=False,default='Available')
#     Price=models.IntegerField(max_length=100,blank=False)

#     def __str__(self):
#         return f'{self.Price}(self.Status)'