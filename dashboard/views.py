from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def import_data(request):
    return render(request,"import.html")

def tables(request):
    return render(request,"tables.html")

def export(request):
    return render(request,"export.html")



