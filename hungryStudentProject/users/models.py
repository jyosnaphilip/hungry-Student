from django.db import models
from django.contrib.auth.models import User
import uuid

from customadmin.models import Restaurant
from restaurants.models import Food



class Customer_Profile(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_ID = models.UUIDField(default=uuid.uuid4,auto_created=True,primary_key=True)
    image = models.ImageField(upload_to='user_profile',null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True)
    customer_address = models.CharField(max_length=100,default='no address')
    city=models.CharField(max_length=30,default='city')
    country=models.CharField(max_length=30,default='country')
    postal_code = models.IntegerField(null=True)
   
    def __str__(self):
         #String for representing the Model object.
        return f'{self.User_ID}'
    

class Orders(models.Model):
    Order_Id=models.UUIDField(primary_key=True,auto_created=True,default=uuid.uuid4)
    Timestamp=models.DateTimeField(auto_now_add=True,blank=False)
    Restaurant_ID=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Customer_ID=models.ForeignKey('Customer_Profile',on_delete=models.CASCADE)
    CATEGORIES=(
        ('Processing','Processing'),
        ('Accepted','Accepted'),
        ('Declined','Declined'),
        ('Cancelled','Cancelled'),
        ('Refunded','Refunded'),
        ('Complete','Complete')
    )
    Order_Status=models.CharField(max_length=20,choices=CATEGORIES,blank=False,default='Processing')
    Total_Price=models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    def __str__(self):
         #String for representing the Model object.
        return f'{self.Order_Id}'
    
    class Meta:
        ordering=['-Timestamp']
        
class Order_Items(models.Model):
    Order_ID=models.ForeignKey(Orders,on_delete=models.CASCADE)
    Restaurant_ID=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Food_ID=models.ForeignKey(Food,on_delete=models.CASCADE)
    Quantity=models.IntegerField(default=1)
    Unit_Price=models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    def __str__(self):
         #String for representing the Model object.
        return str(self.Order_ID.__str__()) +" - "+str(self.Food_ID.__str__())

class Payment(models.Model):
    Transaction_ID=models.UUIDField(auto_created=True,primary_key=True,default=uuid.uuid4)
    Order_ID=models.ForeignKey(Orders,on_delete=models.CASCADE)
    mode=models.CharField(max_length=10,blank=False,default='upi')
    def __str__(self):
         #String for representing the Model object.
        return str(self.Transaction_ID.__str__())+"-"+str(self.Order_ID.__str__())


class Rest_Feedback(models.Model):
    customer_ID=models.ForeignKey(Customer_Profile,on_delete=models.CASCADE)
    rest_id=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Order_Id=models.ForeignKey('Orders',on_delete=models.CASCADE)
    Description=models.CharField(blank=True,null=True,max_length=100)
    Rating=models.PositiveIntegerField(default=3,blank=False)
    
    def __str__(self):
        return str(self.rest_id.__str__()) +" - "+str(self.customer_ID.__str__())
