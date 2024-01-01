from django.shortcuts import render
def homepage(request):
    return render(request,'homepage.html')

def restIndex(request):
    return render(request,'RestaurantTemp/RestIndex.html')
def addMenu(request):
    return render(request,'RestaurantTemp/menu.html')
def restAnalytics(request):
    return render(request,'RestaurantTemp/analytics.html')
# Create your views here.
