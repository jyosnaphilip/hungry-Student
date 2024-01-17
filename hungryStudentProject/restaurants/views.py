from django.shortcuts import render,redirect
from . models import Food,Restaurant_Food_bridge
from customadmin.models import Restaurant
from django.contrib.auth.models import User
from django.http import HttpResponse

def homepage(request):
    return render(request,'homepage.html')

def restDash(request,rest_id):
    context={'rest_id':rest_id}
    return render(request,'RestaurantTemp/restaurant_dashboard.html',context)

def restAnalytics(request):
    return render(request,'RestaurantTemp/analytics.html')

def menu_pg(request,rest_id):
    menu_items=Food.objects.all()
    bridge_items=Restaurant_Food_bridge.objects.all()

    return render(request,'RestaurantTemp/menu.html',{'rest_id':rest_id,'menu_items':menu_items,'bridge_items':bridge_items})

def addMenu(request, rest_id):
    if request.user.is_authenticated:
        print("Here....")
        if request.POST:
            print("Here....")
            rest_id=request.POST.get('rest_id')
            food_item=request.POST.get('food_name')
            food_category=request.POST.get('food_category')
            food_description=request.POST.get('description')
            food_price=request.POST.get('price')
            food_img=request.POST.get('image')
            menu_item=Food(Food_Name=food_item,Category=food_category,Description=food_description,Image=food_img)
            menu_item.save()
            food=Food.objects.last()
            foodId=food.Food_ID
            bridgeItem=Restaurant_Food_bridge(rest_id=Restaurant.objects.get(rest_id=rest_id),Food_ID=Food.objects.get(Food_ID=foodId),Price=food_price)
            bridgeItem.save()
            print("Here....")
            return redirect('menu_pg',rest_id)
    else:
        return HttpResponse("User is not authenticated.")
    
    menu_items=Food.objects.all()
    bridge_items=Restaurant_Food_bridge.objects.all()
    return render(request,'RestaurantTemp\menu.html',context={'menu_items':menu_items,'bridge_items':bridge_items})




def viewFeedback(request):
    return render(request,'RestaurantTemp/rest_feedback.html')

def viewOrders(request):
    return render(request,'RestaurantTemp/today_orders.html')
