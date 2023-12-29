from django.shortcuts import render
def homepage(request):
    return render(request,'homepage.html')

def restIndex(request):
    return render(request,'RestaurantTemp/RestIndex.html')
def viewOrders(request):
    return render(request,'RestaurantTemp/orders.html')
def restAnalytics(request):
    return render(request,'RestaurantTemp/analytics.html')
# Create your views here.
