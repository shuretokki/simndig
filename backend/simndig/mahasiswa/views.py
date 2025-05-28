from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home_mahasiswa(request):
    if request.user.role != 'mahasiswa':
        return redirect('login_redirect')  
    return render(request, include('mahasiswa/home.html'))
