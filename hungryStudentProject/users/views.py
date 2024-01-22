from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from customadmin.models import Feedback
from customadmin.models import Restaurant , Notification
from django.urls import reverse



def users_index(request):
    return render(request,'users/index.html')


def users_dash(request):
    return render(request,'users/user_dash.html')


def user_login(request):
    return render(request, 'users/user_login.html')


def user_details(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                msg = "Username already exists"
                return render(request , 'users/signin.html' , {'msg':msg})
            else:
                user = User.objects.create_user(first_name = first_name , last_name = last_name , username=username , email = email)
                user.set_password('password')
                user.save()
                return redirect('user_login')
        else:
            msg = "Password doesn't match!"
            return render(request , 'users/signin.html' , {'msg':msg})
    return render(request, 'users/signin.html')

            
        

        


