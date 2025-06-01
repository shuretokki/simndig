from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompleteMahasiswa
from datadiri.models import Mahasiswa
from matakuliah.models import MataKuliah

@login_required
def mahasiswa_home(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
    except Mahasiswa.DoesNotExist:
        return redirect('mahasiswa:complete_profile')

    kelas_list = MataKuliah.objects.filter(mahasiswa=mahasiswa.user)
    return render(request, 'mahasiswa/home.html', {
        'user': mahasiswa.user,
        'daftar_kelas': kelas_list
    })

@login_required
def complete_profile(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        return redirect('mahasiswa:mahasiswa_home')
    except Mahasiswa.DoesNotExist:
        mahasiswa = None

    if request.method == 'POST':
        form = CompleteMahasiswa(request.POST, instance=mahasiswa)
        if form.is_valid():
            mahasiswa = form.save(commit=False)
            mahasiswa.user = request.user
            mahasiswa.save()
            return redirect('mahasiswa:mahasiswa_home')
    else:
        form = CompleteMahasiswa(instance=mahasiswa)

    return render(request, 'mahasiswa/complete_profile.html', {'form': form})

@login_required
def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    return render(request, 'mahasiswa/detail_kelas.html', {'kelas': kelas})
