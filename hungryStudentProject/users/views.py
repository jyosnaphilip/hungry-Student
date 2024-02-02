from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from customadmin.models import Feedback
from customadmin.models import Restaurant , Notification
from restaurants.models import Food,Restaurant_Food_bridge
from .models import Customer_Profile
from django.urls import reverse




def users_index(request):
    
    return render(request,'users/index.html' )


def users_dash(request):
    rest = Restaurant.objects.all()
    food = Food.objects.all()
    return render(request,'users/user_dash.html', {'rest':rest , 'food':food})




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



def detail_view(request, rest_id):
    restaurant = Restaurant.objects.get(rest_id=rest_id)
    food = Food.objects.get(Food_ID=rest_id)
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



            
        

        


