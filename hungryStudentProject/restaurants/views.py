from django.shortcuts import render,redirect
from . models import Food
def homepage(request):
    return render(request,'homepage.html')

def restIndex(request):
    return render(request,'RestaurantTemp/RestIndex.html')

def restAnalytics(request):
    return render(request,'RestaurantTemp/analytics.html')

def addMenu(request):
    if request.POST:
        food_item=request.POST['FoodName']
        food_category=request.POST['Category']
        food_description=request.POST['Description']
        food_price=request.POST['Price']
        food_img=request.POST['Image']
        menu_item=Food(Food_Name=food_item,Category=food_category,Description=food_description,Price=food_price,Image=food_img)
        menu_item.save()
        return redirect('addMenu')
    menu_item=Food.objects.all()
    return render(request,'RestaurantTemp\menu.html',context={'menu_items':menu_item})
# Create your views here.
