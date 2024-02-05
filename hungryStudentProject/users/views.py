from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from customadmin.models import Feedback
from customadmin.models import Restaurant , Notification
from restaurants.models import Food,Restaurant_Food_bridge
from .models import Customer_Profile, Order_Items, Rest_Feedback,Orders
from django.urls import reverse
from django.db.models import Sum





def users_index(request):
    return render(request,'users/index.html' )


def users_dash(request):
    rest = Restaurant.objects.all()
    food = Food.objects.all()
    return render(request,'users/user_dash.html', {'rest':rest , 'food':food})

def detail_view(request, rest_id):
    restaurant = Restaurant.objects.get(rest_id=rest_id)
    bridge = Restaurant_Food_bridge.objects.filter(rest_id=restaurant)
    return render(request, 'users/detail_view.html', {'restaurant': restaurant, 'bridge':bridge})


def user_profile(request, user_id):
    user_profile = Customer_Profile.objects.get(User_ID=user_id)
    return render(request,'users/profile.html',{'user_profile':user_profile})

def user_profileedit(request, user_id):
    user_profile = Customer_Profile.objects.get(User_ID=user_id)
    user = User.objects.get(id=user_id)
    
    if request.method=="POST":
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        user_profile.customer_address = request.POST.get('customer_address')
        user_profile.city = request.POST.get('city')
        user_profile.country = request.POST.get('country')
        user_profile.postal_code = request.POST.get('postal_code')
        user_profile.save()
        return redirect('user_profile', user_id)
    return render(request, 'users/profile_edit.html', {'user_profile': user_profile})


# def user_details(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')
#         if password == cpassword:
#             if User.objects.filter(username=username).exists():
#                 msg = "Username already exists"
#                 return render(request , 'users/signin.html' , {'msg':msg})  
#             else:
#                 user = User.objects.create_user(first_name = first_name , last_name = last_name , username=username , email = email)
#                 user.set_password('password')
#                 user.save()
#                 return redirect('user_login')
#         else:
#             msg = "Password doesn't match!"
#             return render(request , 'users/signin.html' , {'msg':msg})
#     return render(request, 'users/signin.html')




def restaurant_foods(request, rest_id):
    foods = Restaurant_Food_bridge.objects.get(rest_id=rest_id)
    # rest_id=foods.rest_id
    # Food_ID=foods.Food_ID
    # Price=foods.Price
    restaurant=Restaurant.objects.get(rest_id=rest_id)
    # name=restaurant.name
    # menu_item=restaurant.menu_item
    food = Food.objects.get(Food_ID=rest_id)
    # Food_ID=food.Food_ID
    # Food_Name=food.Food_Name
    # CATEGORIES=food.CATEGORIES
    # Category=food.Category
    # Description=food.Description
    return render(request, 'users/detail_view.html', {'foods': foods,'restaurant':restaurant,'food':food})


def userdashboard(request, id):
    rest=Restaurant.objects.all()
    customer_ID=Customer_Profile.objects.get(User_ID=id)
    # order = Orders.objects.all()
    order_count = Orders.objects.filter(Customer_ID=customer_ID.customer_ID).count()
    total_amount = Orders.objects.filter(Customer_ID=customer_ID.customer_ID).aggregate(total_amount=Sum('Total_Price'))['total_amount'] or 0
    # restaurants_count = rest.count()
    # print(restaurants_count,"hgkhgjgjg")
    return render(request, 'users/order_now/userdashboard.html', {'id':id,'rest': rest,'order_count':order_count,'total_amount':total_amount})

def orderOptions(request,id):
    rest=Restaurant.objects.all()
    return render(request,'users/order_now/order_options.html',{'rest':rest})
def orderMenu(request,rest_id):
    menu_items=get_object_or_404(Restaurant,rest_id=rest_id)
    bridge=Restaurant_Food_bridge.objects.all()    
    return render(request,'users/order_now/order_menu.html',{'rest_id':rest_id,'menu_items':menu_items,'bridge':bridge})
def givenFeedback(request,id):
    customer_ID=Customer_Profile.objects.get(User_ID=id)
    feedbacks=Rest_Feedback.objects.filter(customer_ID=customer_ID.customer_ID)
    return render(request,'users/order_now/givenFeedback.html',{'feedbacks':feedbacks})
def user_orders(request,id):
    customer_ID=Customer_Profile.objects.get(User_ID=id)
    orders=Orders.objects.filter(Customer_ID=customer_ID.customer_ID)
    feedbacks=Rest_Feedback.objects.filter(customer_ID=customer_ID.customer_ID)
    
    return render(request,'users/order_now/user_orders.html',{'orders':orders,'feedbacks':feedbacks})
        
def addFeedback(request,id,order_id):
    if request.method=='POST':
        customer_ID=Customer_Profile.objects.get(User_ID=id)
        rest=Orders.objects.get(Order_Id=order_id)
        rest_id=rest.Restaurant_ID.rest_id
        description=request.POST['description'].strip()
        rating=request.POST.get('rating')
        feedback=Rest_Feedback(customer_ID=customer_ID,rest_id=Restaurant.objects.get(rest_id=rest_id),Order_Id=Orders.objects.get(Order_Id=order_id),Description=description,Rating=rating)
        feedback.save()
        rest.feedback=True
        rest.save()
        return redirect('user_orders',id)
    return redirect('user_orders',id)

def cancelOrder(request,order_id,id):
    order=Orders.objects.get(Order_Id=order_id)
    order.Order_Status='Cancelled'
    order.save()
    return redirect('user_orders',id)
   
# def userDashboard(request,id):
    
#     return render(request,'users/order_now/userdashboard.html',{'id':id})

        


