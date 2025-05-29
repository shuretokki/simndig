from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import UserRegistrationForm  # Assuming you have a form for registration

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'authenticate/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)  # Redirect to a home page or dashboard
        else:
            error_message = 'Invalid username or password.'
    
    return render(request, 'authenticate/login.html', {'error': error_message})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

@login_required
def home_view(request):
    return render(request, 'home/home.html')

class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to login page if not authenticated
    redirect_field_name = 'redirect_to'  # Name of the query parameter to redirect after login

    def get(self, request):
        return render(request, 'authenticate/protected.html')