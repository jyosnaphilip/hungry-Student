from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Feedback
from .models import Restaurant , Notification
from users.models import Orders,Rest_Feedback
from restaurants.models import Food
from users.models import Order_Items,Orders
from django.urls import reverse
from django.db.models import Sum


# Credentials(Fathima)
@never_cache
@login_required(login_url ="login" )
def admin_index(request):
    noti = Notification.objects.filter(is_read = False).order_by('-created_at')
    total = User.objects.filter(is_superuser = False).count()
    order = Orders.objects.count()
    top_5_restaurants = Orders.objects.order_by('Total_Price')[:5]
    top_food_totals = Order_Items.objects.all().annotate(total_quantity=Sum('Quantity')).order_by('-total_quantity')[:5]
    rest = User.objects.filter(is_superuser = False , is_staff = True)
    rest_count = rest.count()
    user = User.objects.filter(is_superuser = False , is_staff = False)
    user_count = user.count()
    count = noti.count()
    val = count , user_count , rest_count
    datas = list(val)
    return render(request, 'adminTemp/admin/adminindex.html' , {'noti':noti , 'count':count , 'rest_count':rest_count , 'user_count':user_count , 'total':total, 'datas':datas,'order':order, 'top_5_restaurants': top_5_restaurants, 'top_food_totals':top_food_totals})

def read_msg(request , msg_id):
    noti = Notification.objects.get(id = msg_id)
    noti.is_read = True
    noti.save()
    return redirect('admin')
    


def rest_dashboard(request):
    return render(request , 'adminTemp/restaurant/rest_dashboard.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None and user.is_active:
            if user.is_superuser == True:
                login(request , user)
                messages.success(request,'Sucessfully Logged In....')
                return redirect(reverse('admin'))
            # return redirect('admin_login')
                
            if user.is_staff == True and user.is_superuser == False:
                login(request , user)
                restaurant= Restaurant.objects.get(user_id=user)
                rest_id=restaurant.rest_id           
                return redirect('RestDashboard',rest_id)
         
            if user.is_active == True:
                login(request, user)
                return redirect('users_dash')
        else:
            print('wrong')
            msg = "Wrong credentials"
            return render(request , 'adminTemp/admin/login.html' , {'msg':msg})
    return render(request, 'adminTemp/admin/login.html')

   
            # if user.is_superuser == False and user.is_staff == False and user.is_active == True:
            #     login(request , user)
            #     restaurant= Restaurant.objects.get(user_id=user)
            #     rest_id=restaurant.rest_id           
            #     return redirect('RestDashboard',rest_id)
            



def admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')


        if password==confirmpassword:
            user = User.objects.filter(username=username)
            if user.exists():
                msg  ="Username Already Exists!"
                return render(request, 'adminTemp/admin/register.html')
            else:
                first_name = request.POST.get('firstname')
                last_name =  request.POST.get('lastname')
                password = request.POST.get('password')
                new_user=User.objects.create(first_name=first_name,last_name=last_name, password=password)
                new_user.set_password(password)
                messages.success(request,'Account Created Successfully ')
                new_user.save()
                return redirect('login')
            

    else:
        msg = 'Password entered is Incorrect'
        return render(request,'adminTemp/admin/register.html',{'msg':msg})
                

    
def forgot_password(request , user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

    return render(request, 'adminTemp/admin/forgot-password.html')






# All Users Display(Admin Fathima)--------------------------------------------------------------------------------------------------------------------------

def tables(request):
    users = User.objects.all()
    return render(request, 'adminTemp/admin/tables.html' , {'users':users})

def status_changetables(request , user_id):
    users = User.objects.get(id=user_id)
    if users.is_active == False:
        users.is_active = True
        users.save()
        return redirect('tables')
    else:
        users.is_active = False
        users.save()
        return redirect('tables')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

# Restaurents(Admin_Only_Fathima)--------------------------------------------------------------------------------------------------------------------------

def rest(request):
    users = User.objects.filter(is_staff = True , is_superuser = False)
    return render(request ,'adminTemp/admin/restaurents/rest_list.html' , {'users':users})



def status_changerest(request , user_id):
    users = User.objects.get(id=user_id)
    if users.is_active == False:
        users.is_active = True
        users.save()
        return redirect('rest')
    else:
        users.is_active = False
        users.save()
        return redirect('rest')
    

def create_rest(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if cpassword == password:
            if User.objects.filter(username=username).exists():
                msg = "Username already exists!"
                return render(request , 'adminTemp/admin/restaurents/create_rest.html' , {'msg':msg})
                
            else:
                users = User.objects.create_user(first_name=first_name , username=username , email=email)
                users.set_password(password)
                users.is_staff = True
                users.save()
                noti = Notification.objects.create(user=users , message="A new user Signed up")
                noti.save()
                return redirect('rest')
    msg ="Hello"
    return render(request , 'adminTemp/admin/restaurents/create_rest.html' , {'msg' : msg})

def edit_rest(request , user_id):
    user = User.objects.get(id=user_id)
    if request.method =="POST":
        user.first_name = request.POST.get('fname')
        user.email = request.POST.get('email')
        user.save()
        return redirect('rest')
    return render(request , 'adminTemp/admin/restaurents/rest_edit.html' , {'user':user})

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Users (Admin_Only Fathima)--------------------------------------------------------------------------------------------------------------------------

def users(request):
    mainusers = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request,'adminTemp/admin/users/user_list.html',{'mainusers':mainusers})


def create_user(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')


        if password==cpassword:
            if User.objects.filter(username=username).exists():
                mess = "The User already exists"
                return render(request,'adminTemp/admin/users/create_user.html' , {'mess':mess}) 
            
            else:
                users = User.objects.create_user(first_name = first_name,last_name=last_name,username = username, email=email)  
                users.set_password(password)
                users.save()
                return redirect('users')

    return render(request,'adminTemp/admin/users/create_user.html' )


def status_changeuser(request , user_id):
    users = User.objects.get(id=user_id)
    if users.is_active == False:
        users.is_active = True
        users.save()
        return redirect('users')
    else:
        users.is_active = False
        users.save()
        return redirect('users')
    
    
def edit_user(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method =="POST":
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.save()
        return redirect('users')
    return render(request,'adminTemp/admin/users/user_edit.html' , {'user':user})

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Feedback Form (Admin_Fathima) --------------------------------------------------------------------------------------------------------------------------

def feedback(request):
    feedbacks = Rest_Feedback.objects.all()
    return render(request, 'adminTemp/admin/Feedback/feedbacklist.html',{'feedbacks':feedbacks})

def feedbackform(request):
    return render(request, 'adminTemp/admin/Feedback/feedbackform.html')  #Ujain's Work


# Restaurants Table(Admin_Fathima)
def RestaurantDetails(request):
    resttable = Restaurant.objects.all()
    return render(request, 'adminTemp/admin/RestaurantTable/restaurantdetails.html',{'resttable':resttable})


def status_changedetails(request , email):
    users = Restaurant.objects.get(email_id=email)
    if users.status == False:
        users.status = True
        users.save()
        return redirect('RestaurantDetails')
    else:
        users.status = False
        users.save()
        return redirect('RestaurantDetails')
    

def rest_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render (request,'adminTemp/restaurant/users_list.html',{'users':users})

def user_status_change(request , user_id):
    user = User.objects.get(id = user_id)
    if user.is_active == True:
        user.is_active = False
        user.save()
        return redirect('rest_users')
    elif user.is_active == False:
        user.is_active = True
        user.save()
        return redirect('rest_users')
    
def rest_edit_user(request , user_id):
    user = User.objects.get(id = user_id)
    if request.method =="POST":
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.save()
        return redirect('rest_users')
    return render(request , 'adminTemp/restaurant/rest_edit_user.html' , {'user':user})

def create_profile(request , user_id):
    if Restaurant.objects.filter(user_id = user_id).exists():   
        user = Restaurant.objects.get(user_id = user_id)
        return render(request , 'adminTemp/restaurant/rest_profile.html' , {'user':user})
    else:
        return render(request , 'adminTemp/restaurant/create_rest_profile.html')
    
def create_rest_profile(request , user_id):
    user = User.objects.get(id = user_id)
    if request.method == "POST":
        first_name = request.POST.get('fname')
        location = request.POST.get('location')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        image = request.FILES['image']
        user_id = request.POST.get('user_id')
        users = Restaurant.objects.create(name = first_name,location = location, phone_number =phonenumber, email_id=email, image=image, user_id= user_id )
        users.save()
        return render(request, 'adminTemp/restaurant/rest_profile.html')
    return render(request , 'adminTemp/restaurant/create_rest_profile.html' , {'user':user})
    
def rest_profile(request , user_id):
    user = Restaurant.objects.get(user_id = user_id)
    return render(request , 'adminTemp/restaurant/rest_profile.html' , {'user':user})

def edit_rest_profile(request , user_id):
    rest = Restaurant.objects.get(user_id = user_id)
    if request.method == "POST":
        rest.name = request.POST.get('fname')
        rest.location = request.POST.get('location')
        rest.phone_number = request.POST.get('phonenumber')
        rest.email_id = request.POST.get('email')
        if 'new_image' in request.FILES and request.FILES['new_image'].size > 0:
            img = request.FILES['new_image']
        elif 'image' in request.POST and request.POST['image']:
            img = request.POST.get('image')
        rest.image = img
        rest.user_id = request.POST.get('user_id')
        rest.save()
        return redirect('rest_profile' , user_id = user_id)
    return render(request , 'adminTemp/restaurant/rest_edit_profile.html' , {'rest':rest})

def fpassword(request , user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            user.set_password('password')
            user.save()
            return redirect('rest')
        else:
            msg = "Password didn't match!"
            return render(request , 'adminTemp/admin/forgot-password.html' , {'msg':msg})
    return render(request , 'adminTemp/admin/forgot-password.html')
    



def show_orders(request):
    bridge_rest_id = Order_Items.objects.all()
    return render(request, 'adminTemp/admin/Order/orders.html', {'rest_name': bridge_rest_id})


def edit_order(request,order_id):
    order = Orders.objects.get(Order_Id=order_id)
    if request.method == "POST":
        order.Order_Status = request.POST.get("status")
        order.save()
        return redirect('show_orders')

    return render(request,'adminTemp/admin/Order/edit_order.html',{'order':order})






# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------







