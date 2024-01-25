from django.contrib import admin
from users.models import Customer_Profile, Orders,Order_Items,Payment
# Register your models here.
admin.site.register(Customer_Profile)
admin.site.register(Orders)
admin.site.register(Order_Items)
admin.site.register(Payment)

