from django.shortcuts import render,redirect,get_object_or_404
from matplotlib.markers import MarkerStyle

from restaurants.models import Food,Restaurant_Food_bridge
from customadmin.models import Restaurant
from users.models import Customer_Profile,Order_Items,Orders,Rest_Feedback
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
import plotly.express as px
import pandas as pd
from plotly.offline import plot
from django.db.models.functions import Cast
from django.db.models import TextField

def homepage(request):
    return render(request,'homepage.html')

#------------------------------------------------------------------------------------------
# restaurant_dashboard.html
def newOrders(rest_id):
    pending=Orders.objects.filter(Restaurant_ID=rest_id,Order_Status='Processing').count()
    return pending

def pendingOrders(rest_id):
    pending=Orders.objects.filter(Restaurant_ID=rest_id,Order_Status='Accepted').count()
    return pending

def ordersServed(rest_id):
    served=Orders.objects.filter(Restaurant_ID=rest_id,Order_Status='Complete').count()
    return served

def mostOrdered(rest_id):
    food_items=Restaurant_Food_bridge.objects.filter(rest_id=rest_id) #has all unique food items of rest
    max_v=0                                                 #initialise variable that stores the max of total quantity
    max_id=0                                      # initialise variable that stores the fod id with highest totat quant
    for item in food_items:                                        # iterate through each food item
        item_ID=item.Food_ID                                    #take each item's  id
        max_q=sum(Order_Items.objects.filter(Restaurant_ID=rest_id,Food_ID=item_ID).values_list('Quantity',flat=True)) 
                   #filter by restid and food id, then obtain the resultants quantity in list form. then get sum of list
                  # bubblesort

        if max_q>max_v:
            max_v=max_q
            max_id=item_ID
    if max_id!=0:                                                # for restaurants that have had atleast one order
        return max_id.Food_Name,max_v    
    else:
        return "na","na"    #will through an eror if this is not there, when the restaurant is signing up for 
                             #first time and has no orders yet.
    

def totalEarned(rest_id):
    earning=sum(Orders.objects.filter(Restaurant_ID=rest_id).values_list('Total_Price',flat=True))
    return earning


def itemRevenue(rest_id): #should return a dictionary with each food_id as key and the amount obtained from each of them as value
    revenue_all={'item':[],'tot_sales':[]}
    food_items=Restaurant_Food_bridge.objects.filter(rest_id=rest_id).annotate(str_item_id=Cast('Food_ID',output_field=TextField())).values_list('str_item_id')
    
    for item in food_items:
        item_id=item[-1] #gets food_id! at 0 index this doesnt work!
        revenue_each=Order_Items.objects.filter(Food_ID=item_id).values_list('Unit_Price','Quantity')
        item_name=(Food.objects.get(Food_ID=item_id)).Food_Name    #get the row having itemid, then extract name
        revenue_all['item'].append(item_name)
        total=0
        for i in revenue_each:
            total+=i[0]*i[1]
        if total!=0:
            revenue_all['tot_sales'].append(float(total))
        else:
            revenue_all['tot_sales'].append(0)
    df=pd.DataFrame.from_dict(revenue_all)
    return df

def categoryAnalysis(rest_id):
    cat_dict={'category':['Starter','Main Course','Dessert','Beverage'],'Quantity_Sold':[0,0,0,0]}
    items_id=Order_Items.objects.filter(Restaurant_ID=rest_id).annotate(str_food_id=Cast('Food_ID',output_field=TextField())).values_list('str_food_id')
    for item in items_id:
        item_id=item[-1]
        cat=Food.objects.get(Food_ID=item_id).Category
        print(cat)
        instances=sum(Order_Items.objects.filter(Food_ID=item_id).values_list('Quantity',flat=True))
        if cat=='Starter':
            cat_dict['Quantity_Sold'][0]+=instances
        elif cat=='Main Course':
            cat_dict['Quantity_Sold'][1]+=instances
        elif cat== 'Dessert':
            cat_dict['Quantity_Sold'][2]+=instances
        else: 
            cat_dict['Quantity_Sold'][3]+=instances
    df=pd.DataFrame.from_dict(cat_dict)
    return df
    


def restDash(request,rest_id):
    new=newOrders(rest_id)
    pending=pendingOrders(rest_id)
    served=ordersServed(rest_id)
    popular,num=mostOrdered(rest_id)
    earnings=totalEarned(rest_id)
    bar_df=itemRevenue(rest_id)
    pie_df=categoryAnalysis(rest_id)
    pie_chart=px.pie(pie_df,values='Quantity_Sold',names='category',hole=0.5,height=300)
    bar_chart=px.bar(bar_df,x='item',y='tot_sales',height=320,labels={'item':'Food Item','tot_sales':'Sales'})
    barChartOutput=bar_chart.to_html(full_html=False,include_plotlyjs=False)
    pieChartOutput=pie_chart.to_html(full_html=False,include_plotlyjs=False)
    context={'rest_id':rest_id,'new':new,'served':served,'popular':popular,'num':num,'earnings':earnings,"pending":pending,'barChartOutput':barChartOutput,'pieChartOutput':pieChartOutput}
    return render(request,'RestaurantTemp/restaurant_dashboard.html',context)


#----------------------------------------------------------------------------------------
#menu.html
def menu_pg(request,rest_id):
     #function that renders menu _items pg
    new=newOrders(rest_id)
    menu_items=get_object_or_404(Restaurant,rest_id=rest_id)
    bridge_items=Restaurant_Food_bridge.objects.all().order_by('Status')
    return render(request,'RestaurantTemp/menu.html',{'rest_id':rest_id,'menu_items':menu_items,'bridge_items':bridge_items,'new':new})

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
            food_img=request.FILES.get('image')
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

#---------------------------------------------------------------------------------------------------------

#create_rest_profile.html
def viewRestProfile(request,rest_id):    
    rest_details=Restaurant.objects.get(rest_id=rest_id)
    
    return render(request,'RestaurantTemp/create_rest_profile.html',context={'rest_id':rest_id,'rest_details':rest_details,'media_url':settings.MEDIA_URL})

def editRestProfile(request,rest_id):
    rest_details=Restaurant.objects.get(rest_id=rest_id)
    if request.method == "POST":
            print('here')
            rest_details.phone_number=request.POST.get('rest_phone')
            rest_details.location=request.POST.get('rest_location')
            rest_details.image=request.FILES.get('idImage1')
            rest_details.save()
            return redirect('viewProfile',rest_id)
    return redirect('RestaurantTemp\create_rest_profile.html',rest_id)

#-----------------------------------#-------------------------------------------------------#
#today_orders.html
def viewOrders(request,rest_id):
    new=newOrders(rest_id)
    rest_orders=Orders.objects.filter(Restaurant_ID=rest_id)
    customers=Customer_Profile.objects.all()
    return render(request,'RestaurantTemp/today_orders.html',{'rest_id':rest_id,'orders':rest_orders,'customers':customers,'new':new})

def acceptOrder(request,Order_Id):
    order=Orders.objects.get(Order_Id=Order_Id)
    order.Order_Status='Accepted'
    order.save()
    rest_id=order.Restaurant_ID
    rest_orders=Orders.objects.filter(Restaurant_ID=rest_id)
    customers=Customer_Profile.objects.all()
    return render(request,'RestaurantTemp/today_orders.html',{'rest_id':rest_id,'orders':rest_orders,'customers':customers})

def declineOrder(request,Order_Id):
    order=Orders.objects.get(Order_Id=Order_Id)  #getting that particular order
    order.Order_Status='Declined'                #changing order status
    order.save()                                 #saving it to db
    rest_id=order.Restaurant_ID                  #getting rest id to pass as its a necc paraMETER for the redirected page
    rest_orders=Orders.objects.filter(Restaurant_ID=rest_id)    #get all orders of restaurant
    customers=Customer_Profile.objects.all()             #get the name of customers as well,and send everything to temp
    return render(request,'RestaurantTemp/today_orders.html',{'rest_id':rest_id,'orders':rest_orders,'customers':customers})

#====================================================#==============================================#
#rest_feedback.html
def viewFeedback(request,rest_id):
    new=newOrders(rest_id)
    feedbacks=Rest_Feedback.objects.filter(rest_id=rest_id)
    order_items=Order_Items.objects.all()
    return render(request,'RestaurantTemp/rest_feedback.html',{'rest_id':rest_id,'feedbacks':feedbacks,'order_items':order_items,'new':new})


#=======================================================#==========================================#

#search in menu
def searchMenu(request,rest_id):
    if request.method == 'POST':
        query=request.POST['search_query']
        outputs=Food.objects.filter(restaurant_food_bridge__rest_id__rest_id=rest_id,Food_Name__icontains=query)
        return render(request, 'RestaurantTemp/searchResults.html',{'query':query, 'outputs':outputs,'rest_id':rest_id})
    else:
        return render(request, 'RestaurantTemp/searchResults.html',{rest_id:rest_id})

#================================#==========================================================#




   