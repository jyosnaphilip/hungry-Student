from django.shortcuts import render,redirect,get_object_or_404

from restaurants.models import Food,Restaurant_Food_bridge
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

def menu_pg(request,rest_id): #function that renders menu _items pg
    menu_items=get_object_or_404(Restaurant,rest_id=rest_id)
    bridge_items=Restaurant_Food_bridge.objects.all()
    return render(request,'RestaurantTemp/menu.html',{'rest_id':rest_id,'menu_items':menu_items,'bridge_items':bridge_items})

def addMenu(request, rest_id):     #function to save items, runs when new menu item added
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
            bridgeItem=Restaurant_Food_bridge(rest_id=Restaurant.objects.get(rest_id=rest_id),Food_ID=menu_item,Price=food_price)### is this the error, try removing get
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

def editMenu(request,Food_ID):
    item = Food.objects.get(Food_ID=Food_ID)
    item_bridge=Restaurant_Food_bridge.objects.get(Food_ID=Food_ID)
    rest_id=item_bridge.rest_id.rest_id
    if request.method =="POST":
        item.Food_Name = request.POST['edit-'+Food_ID].strip()
        item_bridge.Price = request.POST['editPrice-'+Food_ID]
        item.Description=request.POST['editdesc-'+Food_ID]
        item.save()
        item_bridge.save()
        return redirect('menu_pg',rest_id)
    return redirect('menu_pg',rest_id)

def delMenuItem(request, Food_ID,rest_id):
    item=Food.objects.get(Food_ID=Food_ID)
    item_bridge=Restaurant_Food_bridge.objects.get(Food_ID=Food_ID)
    rest_id=rest_id
    item.delete()
    item_bridge.delete()
    return redirect('menu_pg',rest_id)

def toggle_status(request,Food_ID,rest_id):
    bridge_item=Restaurant_Food_bridge.objects.get(Food_ID_id=Food_ID,rest_id_id=rest_id)
    if bridge_item.Status == True:
        bridge_item.Status=False
    else:
        bridge_item.Status=True
    bridge_item.save()
    return redirect('menu_pg',rest_id) 
