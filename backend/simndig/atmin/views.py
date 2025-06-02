from django.shortcuts import render

def home(request):
    return render(request, 'atmin/home.html')
