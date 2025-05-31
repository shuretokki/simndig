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

def detail_kela(request, kelas_id):
    kelas = get_object_or_404(matakuliah, id=kelas_id)
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})