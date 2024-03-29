"""
URL configuration for hungryStudentProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from restaurants.views import homepage,restDash,addMenu,addMenu,viewFeedback,menu_pg,editMenu,delMenuItem,toggle_status,viewRestProfile,editRestProfile,viewOrders,acceptOrder,declineOrder,searchMenu
from customadmin.views import admin_index, admin_login, admin_register,forgot_password,tables , status_changeuser  , rest , create_rest , edit_rest, users, create_user, edit_user, feedback, feedbackform , admin_logout, RestaurantDetails, status_changerest, status_changetables, status_changedetails , rest_dashboard , rest_users , user_status_change , rest_edit_user , create_profile ,  create_rest_profile , rest_profile , edit_rest_profile , read_msg , fpassword,show_orders,edit_order,user_logout
from users.views import  addFeedback, users_index,users_dash,detail_view,user_profile,user_profileedit,userdashboard,orderOptions,orderMenu,givenFeedback,user_orders,addFeedback,cancelOrder
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',homepage,name='home'),
    path('Restaurants/<str:rest_id>',restDash,name='RestDashboard'),
    # related to menu
    path('Restaurants/menu/<str:rest_id>',menu_pg, name ='menu_pg'), #function that renders menu _items pg
    path('Restaurants/addmenu/<str:rest_id>',addMenu, name ='addMenu'),  #function to save items, runs when new menu item added
    path('Restaurants/edit-menu/<str:Food_ID>',editMenu,name='editMenu'),
    path('restaurant/del-Menu-Item/<str:Food_ID>/<str:rest_id>',delMenuItem,name='delete-item'),
    path('restaurants/toggle-status/<str:Food_ID>/<str:rest_id>',toggle_status,name='toggle_status'),
    

    path('Restaurants/view_feedback/<str:rest_id>',viewFeedback, name='view-feedback'), #feedback
    # related to view orders
    path('Restaurants/view_orders/<str:rest_id>',viewOrders, name='today-orders'),
    path('restaurants/accept-order/<str:Order_Id>',acceptOrder,name='accept'),
    path('restaurants/decline-order/<str:Order_Id>',declineOrder,name='decline'),
    #related to rest profile
    path('Restaurants/ViewProfile/<str:rest_id>',viewRestProfile, name='viewProfile'),
    path('Restaurants/edit_profile/<str:rest_id>',editRestProfile,name="edit_profile"),
    #for search bar in restaurants
    path('Restaurants/searchMenu/<str:rest_id>',searchMenu, name='searchMenu'),
    #for actual working user dashboard
    path('user/a-dashboard/<int:id>',userdashboard,name='userdashboard'),
    path('user/orderoptions/<int:id>',orderOptions,name='orderOptions'),
    path('user/orderMenu/<str:rest_id>',orderMenu,name='orderMenu'),
    path('user/givenFeedback/<int:id>',givenFeedback,name='givenFeedback'),
    path('user/user_orders/<int:id>',user_orders,name='user_orders'),
    path('user/add_feedback/<int:id>/<str:order_id>',addFeedback,name='addFeedback'),
    path('user/cancelOrder/<str:order_id>/<int:id>',cancelOrder,name='cancelOrder'),
   
    

    # Dashboard(Fathima)
    path('Dashboard', admin_index,name = 'admin'),
    path('read_msg/<int:msg_id>' , read_msg , name="read_msg"),
    path('rest_dashboard/<str:rest_id', rest_dashboard,name = 'rest_dashboard'),
    
    #Admin Side(Fathima)
    path('',users_index,name='users_index'),
    path('login',admin_login, name='login'),
    path('forgotpassword/<int:user_id>' , fpassword , name="fpassword"),
    path('admin_logout',admin_logout, name='admin_logout'),
    path('user_logout',user_logout,name='user_logout'),
    path('Register',admin_register,name = 'register'),
    path('ForgotPassword',forgot_password,name = 'forgotpassword' ),
    path('tables',tables,name = 'tables'),
    path('status_changetables/<int:user_id>' ,status_changetables , name="status_changetables"),

# Restaurants(Fathima)
    path('rest',rest,name = 'rest' ),
    path('create_rest',create_rest,name = 'create_rest' ),
    path('status_changerest/<int:user_id>' ,status_changerest , name="status_changerest"),
    path('edit_rest/<int:user_id>' ,edit_rest , name="edit_rest"),

# Users(Fathima)
    path('users',users,name = 'users'),
    path('create_user',create_user, name = 'create_user'),
    path('inactive_btn/<int:user_id>',status_changeuser,name='status_changeuser'),
    path('edit_user/<int:user_id>',edit_user, name = 'edit_user'),


# Feedback(Fathima)
    path('Feedback>',feedback,name='feedbacklist'),
    path('Feedbackform',feedbackform,name = 'feedbackform'),


#Restaurant Details (Fathima)
    path('RestaurantDetails',RestaurantDetails,name = 'RestaurantDetails'),
    path('status_changedetails/<str:email>',status_changedetails,name = 'status_changedetails'),

# Users (Fathima)
    path('rest_users',rest_users,name = 'rest_users'),
    path('user_status_change/<int:user_id>',user_status_change,name = 'user_status_change'),
    path('rest_edit_user/<int:user_id>',rest_edit_user,name = 'rest_edit_user'),
    path('create_profile/<int:user_id>',create_profile,name = 'create_profile'),
    path('rest_profile/<int:user_id>',rest_profile,name = 'rest_profile'),
    path('create_rest_profile/<int:user_id>' , create_rest_profile , name='create_rest_profile'),
    path('edit_rest_profile/<int:user_id>' , edit_rest_profile , name="edit_rest_profile"),

    
# Orders(Fathima)
    path('show_orders',show_orders,name='show_orders'),
    path('edit_order/<uuid:order_id>/',edit_order,name='edit_order'),

    #Users-Ujain's Part(Fathima)
    path('users_index',users_index,name='users_index'),
    path('users_dash',users_dash,name='users_dash'),
    path('detail_view/<uuid:rest_id>',detail_view,name='detail_view'),
    path('user_profile/<int:user_id>',user_profile, name='user_profile'),
    path('user_profileedit/<int:user_id>',user_profileedit,name='user_profileedit'),
    # path('restaurant/<uuid:rest_id>/foods/', restaurant_foods, name='restaurant_foods'),


    # path('users_dash/<str:rest_id>',users_dash,name='users_dash'),
    # path('')

]


# Restaurant Table (Fathima)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)