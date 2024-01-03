from django.contrib import admin
from .models import Feedback
from .models import Restaurant , Notification




# Fathima(Admin)
admin.site.register(Feedback)
admin.site.register(Restaurant)
admin.site.register(Notification)