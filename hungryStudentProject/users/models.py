from django.db import models
from django.contrib.auth.models import User


class Users_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_profile',null=True,blank=True)
    customer_address = models.CharField(max_length=100)
    city=models.CharField(max_length=30)
    country=models.CharField(max_length=30)
    postal_code = models.IntegerField()
    
    # customer_id = models.IntegerField(primary_key = True)
    # name = models.CharField(max_length=30)
    # phonenumber = models.CharField(max_length =30)
    # emailid = models.CharField(max_length = 30)
    



