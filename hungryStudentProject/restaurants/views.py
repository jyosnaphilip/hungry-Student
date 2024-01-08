from django.shortcuts import render,redirect
from . models import Food
from customadmin.models import Restaurant
def homepage(request):
    return render(request,'homepage.html')

def restIndex(request):
    return render(request,'RestaurantTemp/restaurant_dashboard.html')

def restAnalytics(request):
    return render(request,'RestaurantTemp/analytics.html')

def addMenu(request):
    if request.POST:
        food_item=request.POST['FoodName']
        food_category=request.POST['Category']
        food_description=request.POST['Description']
        food_price=request.POST['Price']
        food_img=request.POST['Image']
        menu_item=Food(Food_Name=food_item,Category=food_category,Description=food_description,Image=food_img)
        menu_item.save()
        food_id=menu_item.Food_ID
        return redirect('addMenu')
    menu_item=Food.objects.all()
    return render(request,'RestaurantTemp\menu.html',context={'menu_items':menu_item})

def viewFeedback(request):
    return render(request,'RestaurantTemp/rest_feedback.html')

def viewOrders(request):
    return render(request,'RestaurantTemp/today_orders.html')
