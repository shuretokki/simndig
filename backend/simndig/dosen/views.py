from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datadiri.models import Dosen  # Import directly from datadiri
from .forms import DosenInitialProfileForm, DosenAdvancedProfileForm
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

    # Dummy Kelas Wajib
    for i in range(1, random.randint(2, 4)):  # Generate 1 to 3 dummy wajib courses
        kode_mk = f"{base_kode_mk}W{i}"
        if not KelasWajib.objects.filter(kode_mk=kode_mk).exists():
            KelasWajib.objects.create(
                _nama=f"Dummy Mata Kuliah Wajib {i} ({user.username})",
                kode_mk=kode_mk,
                sks=random.choice([2, 3, 4]),
                semester=random.randint(1, 8),
                dosen=user,
                _nim=f"NIM-MK-W{i}",  # Placeholder for MataKuliah._nim
                # Placeholder for MataKuliah.email
                email=f"mk-w{i}@example.com"
            )

    # Dummy Kelas Pilihan
    for i in range(1, random.randint(2, 3)):  # Generate 1 to 2 dummy pilihan courses
        kode_mk = f"{base_kode_mk}P{i}"
        if not KelasPilihan.objects.filter(kode_mk=kode_mk).exists():
            KelasPilihan.objects.create(
                _nama=f"Dummy Mata Kuliah Pilihan {i} ({user.username})",
                kode_mk=kode_mk,
                sks=random.choice([2, 3]),
                semester=random.randint(3, 8),
                dosen=user,
                _nim=f"NIM-MK-P{i}",  # Placeholder for MataKuliah._nim
                # Placeholder for MataKuliah.email
                email=f"mk-p{i}@example.com"
            )

    dosen_profile.dummy_courses_generated = True
    dosen_profile.save(update_fields=['dummy_courses_generated'])


@login_required
def dosen_home(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
        if not dosen.advanced_profile_completed:
            # Check if initial profile step was done by checking a field like NIP
            if not dosen.nip:  # Or another field from the initial form
                messages.info(request, 'Silakan lengkapi profil awal Anda.')
                return redirect('dosen:complete_initial_profile')
            messages.info(request, 'Silakan lengkapi profil lanjutan Anda.')
            return redirect('dosen:complete_advanced_profile')
    except Dosen.DoesNotExist:
        messages.info(
            request, 'Selamat datang! Silakan lengkapi profil dosen Anda.')
        return redirect('dosen:complete_initial_profile')

        # Generate dummy courses if profile is complete but courses not yet generated
    if dosen.advanced_profile_completed and not dosen.dummy_courses_generated:
        generate_dummy_courses(dosen)
        # Refresh dosen object to get updated dummy_courses_generated status if needed,
        # though generate_dummy_courses saves it.

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
        if dosen.advanced_profile_completed:
            return redirect('dosen:dosen_home')
        # If dosen exists but advanced is not complete, they might be here to update initial info
        # or were redirected. Allow filling this form.
    except Dosen.DoesNotExist:
        dosen = None  # Create a new Dosen profile instance

    if request.method == 'POST':
        form = DosenInitialProfileForm(request.POST, instance=dosen)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # Ensure advanced_profile_completed is False until the next step is done
            # This will be handled by the Dosen model's default or explicitly here if needed.
            # profile.advanced_profile_completed = False
            profile.save()
            if not profile.dummy_courses_generated:  # Generate dummy courses upon full profile completion
                generate_dummy_courses(profile)
            messages.success(
                request, 'Profil awal berhasil disimpan. Silakan lengkapi profil lanjutan.')
            return redirect('dosen:complete_advanced_profile')
        else:
            messages.error(request, 'Harap perbaiki kesalahan di bawah ini.')
    else:
        form = DosenInitialProfileForm(instance=dosen)

    return render(request, 'dosen/complete_initial_profile.html', {'form': form})


@login_required
def complete_advanced_profile(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
        if dosen.advanced_profile_completed:
            return redirect('dosen:dosen_home')
    except Dosen.DoesNotExist:
        messages.error(
            request, 'Profil awal tidak ditemukan. Silakan lengkapi profil awal terlebih dahulu.')
        return redirect('dosen:complete_initial_profile')

    if request.method == 'POST':
        form = DosenAdvancedProfileForm(
            request.POST, request.FILES, instance=dosen)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.advanced_profile_completed = True
            profile.save()
            messages.success(request, 'Profil berhasil dilengkapi!')
            return redirect('dosen:dosen_home')
        else:
            messages.error(request, 'Harap perbaiki kesalahan di bawah ini.')
    else:
        form = DosenAdvancedProfileForm(instance=dosen)

    return render(request, 'dosen/complete_advanced_profile.html', {'form': form})
