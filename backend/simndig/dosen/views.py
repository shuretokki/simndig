from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Dosen
from .forms import CompleteDosen
from matakuliah.models import MataKuliah


@login_required
def dosen_home(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
    except Dosen.DoesNotExist:
        return redirect('dosen:complete_profile')

    kelas_list = MataKuliah.objects.filter(dosen=dosen.user)
    return render(request, 'dosen/home.html', {
        'user': dosen.user,
        'daftar_kelas': kelas_list
    })


def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})

@login_required
def complete_profile(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
        return redirect('dosen:dosen_home')
    except Dosen.DoesNotExist:
        dosen = None

    if request.method == 'POST':
        form = CompleteDosen(request.POST, instance=dosen)
        if form.is_valid():
            dosen = form.save(commit=False)
            dosen.user = request.user
            dosen.save()
            return redirect('dosen:dosen_home')
        else:
            # Form tidak valid, error akan ditampilkan di template
            pass
    else:
        form = CompleteDosen(instance=dosen)

    return render(request, 'dosen/complete_profile.html', {'form': form})
