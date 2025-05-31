from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datadiri.models import Dosen  # Import dari datadiri
from matakuliah.models import MataKuliah

@login_required
def dosen_home(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
    except Dosen.DoesNotExist:
        return render(request, 'dosen/profile_not_found.html')

    kelas_list = MataKuliah.objects.filter(dosen=dosen.user)
    return render(request, 'dosen/home.html', {
        'user': dosen.user,
        'daftar_kelas': kelas_list
    })

def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})
