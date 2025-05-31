from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Dosen

@login_required
def home(request):
    dosen = Dosen.objects.get(user=request.user)
    kelas_list = dosen.kelas.list_dosen.all()

    return render(request, 'dosen/home.html', {
        'user' : dosen.user,
        'daftar_kelas' : kelas_list
    })
