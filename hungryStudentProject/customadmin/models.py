from django.db import models
from django.contrib.auth.models import User
import uuid


# class userdetails(models.Models):
#     user = models.ForeignKey(User,on_delete = models.CASCADE)
#     user_phone = models.CharField(max_length = 22)
#     user_type = models.CharField(max_length = 5)

class Feedback(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length = 100)
    message = models.TextField()

    def __str__(self):
        return f"Feedback from {self.name}"
    

class Restaurant(models.Model):
    rest_id = models.UUIDField(default=uuid.uuid4, auto_created = True,editable=False, blank=False, unique=True,primary_key = True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email_id = models.EmailField()
    image = models.ImageField(upload_to='restaurant_images/')
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.BooleanField(default = True)

    def __str__(self):
        return self.name   
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

