from django.shortcuts import render
def homepage(request):
    return render(request,'homepage.html')

def restIndex(request):
    return render(request,'RestaurantTemp/RestIndex.html')

# Create your views here.
