from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datadiri.models import Dosen
from .forms import DosenInitialProfileForm
from matakuliah.models import MataKuliah, KelasWajib, KelasPilihan
from django.contrib import messages
import random
from django.utils import timezone


def generate_dummy_courses(dosen_profile):
    """
    Generates a few dummy courses (KelasWajib and KelasPilihan) for a Dosen.
    Ensures this runs only once.
    """
    if dosen_profile.dummy_courses_generated:
        return

    user = dosen_profile.user
    base_kode_mk = f"DUMMY{user.id}-"

    for i in range(1, random.randint(2, 4)):
        kode_mk = f"{base_kode_mk}W{i}"
        if not KelasWajib.objects.filter(kode_mk=kode_mk).exists():
            # The incorrect _nim and email fields have been removed from this call
            KelasWajib.objects.create(
                _nama=f"Dummy Mata Kuliah Wajib {i} ({user.username})",
                kode_mk=kode_mk,
                sks=random.choice([2, 3, 4]),
                semester=random.randint(1, 8),
                dosen=user,
            )

    for i in range(1, random.randint(2, 3)):
        kode_mk = f"{base_kode_mk}P{i}"
        if not KelasPilihan.objects.filter(kode_mk=kode_mk).exists():
            # The incorrect _nim and email fields have also been removed from this call
            KelasPilihan.objects.create(
                _nama=f"Dummy Mata Kuliah Pilihan {i} ({user.username})",
                kode_mk=kode_mk,
                sks=random.choice([2, 3]),
                semester=random.randint(3, 8),
                dosen=user,
            )

    dosen_profile.dummy_courses_generated = True
    dosen_profile.save(update_fields=['dummy_courses_generated'])


@login_required
def dosen_home(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
        if not dosen.initial_profile_completed:
            if not dosen.nip:
                messages.info(request, 'Silakan lengkapi profil awal Anda.')
                return redirect('dosen:complete_initial_profile')
    except Dosen.DoesNotExist:
        messages.info(
            request, 'Selamat datang! Silakan lengkapi profil dosen Anda.')
        return redirect('dosen:complete_initial_profile')

    if dosen.initial_profile_completed and not dosen.dummy_courses_generated:
        generate_dummy_courses(dosen)

    courses_taught = MataKuliah.objects.filter(
        dosen=dosen.user).select_related('kelaswajib', 'kelaspilihan')

    return render(request, 'dosen/home.html', {'dosen_profile': dosen, 'courses_taught': courses_taught})


def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})


@login_required
def complete_initial_profile(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
    except Dosen.DoesNotExist:
        dosen = None

    if request.method == 'POST':
        form = DosenInitialProfileForm(request.POST, instance=dosen)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if not profile.dummy_courses_generated:
                generate_dummy_courses(profile)
            messages.success(
                request, 'Profil berhasil disimpan')
            return redirect('home')
        else:
            messages.error(request, 'Harap perbaiki kesalahan di bawah ini.')
    else:
        form = DosenInitialProfileForm(instance=dosen)

    return render(request, 'dosen/complete_initial_profile.html', {'form': form})
