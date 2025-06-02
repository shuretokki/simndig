from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
# Assuming you have a form for registration
from .forms import UserRegistrationForm
from .models import UserProfile  # Import model UserProfile


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data.get('role')

            user = User.objects.create_user(
                username=username, password=password)
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            print(
                f"DEBUG: Register User {username} created with role: {profile.role}")

            login(request, user)
            return redirect('home')
        else:
            print("DEBUG: Form errors:", form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_profile = user.userprofile
            role = user_profile.role.lower()

            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)

            if role == 'mahasiswa':
                return redirect(reverse('mahasiswa:mahasiswa_home'))
            elif role == 'dosen':
                return redirect(reverse('dosen:dosen_home'))
            elif role == 'admin':
                return redirect(reverse('atmin:atmin_home'))
            else:
                return redirect('home')
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'accounts/login.html', {'error': error_message, 'next': request.GET.get('next', '')})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')


@login_required
def home_view(request):
    user_profile = request.user.userprofile
    role = user_profile.role.lower()

    # Debugging output
    print(f"User role: {user_profile.role}")

    if role == 'mahasiswa':
        # redirects to /mahasiswa/
        return redirect(reverse('mahasiswa:mahasiswa_home'))
    elif role == 'dosen':
        # redirects to /dosen/
        return redirect(reverse('dosen:dosen_home'))
    elif role == 'admin':
        # redirects to /atmin/
        return redirect(reverse('atmin:atmin_home'))
    else:
        return redirect('login')


class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect to login page if not authenticated
    # Name of the query parameter to redirect after login
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')
