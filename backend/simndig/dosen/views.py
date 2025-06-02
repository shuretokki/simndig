from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datadiri.models import Dosen  # Assumed import
from .forms import DosenInitialProfileForm  # Assumed import
# Keep if generate_dummy_courses uses them
from matakuliah.models import MataKuliah, KelasWajib, KelasPilihan
from django.contrib import messages
import random  # Keep if generate_dummy_courses uses it
from django.utils import timezone  # Keep if generate_dummy_courses uses it


def generate_unique_nip():
    """Generates a random, unique 18-digit NIP."""
    while True:
        nip = f"{timezone.now().strftime('%Y%m%d')}{random.randint(1000000000, 9999999999)}"[
            :18]
        if not Dosen.objects.filter(nip=nip).exists():
            return nip


# Status choices are defined here for use in randomization
DOSEN_STATUS_CHOICES = [
    ('Aktif', 'Aktif'),
    ('Cuti', 'Cuti'),
    ('Studi Lanjut', 'Studi Lanjut'),
    ('Pensiun', 'Pensiun'),
]


def generate_dummy_courses(dosen_profile):
    """
    Generates a few dummy courses (KelasWajib and KelasPilihan) for a Dosen.
    Ensures this runs only once.
    """
    if dosen_profile.dummy_courses_generated:
        return

    user = dosen_profile.user
    base_kode_mk = f"DUMMY{user.id}-"

    # Ensure KelasWajib and KelasPilihan are imported if this function is used
    # from matakuliah.models import KelasWajib, KelasPilihan

    for i in range(1, random.randint(2, 4)):
        kode_mk = f"{base_kode_mk}W{i}"
        if not KelasWajib.objects.filter(kode_mk=kode_mk).exists():
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
            messages.info(
                request, 'Selamat datang! Mohon lengkapi profil awal Anda untuk melanjutkan.')
            return redirect('dosen:complete_initial_profile')
    except Dosen.DoesNotExist:
        messages.info(
            request, 'Selamat datang! Silakan buat profil dosen Anda.')
        return redirect('dosen:complete_initial_profile')

    if not dosen.dummy_courses_generated:
        generate_dummy_courses(dosen)

    courses_taught = MataKuliah.objects.filter(
        dosen=dosen.user).select_related('kelaswajib', 'kelaspilihan')

    return render(request, 'dosen/home.html', {'dosen_profile': dosen, 'courses_taught': courses_taught})


@login_required
def complete_initial_profile(request):
    try:
        dosen = Dosen.objects.get(user=request.user)
    except Dosen.DoesNotExist:
        # If Dosen profile doesn't exist, we'll create a new one if the form is valid.
        # Setting dosen to None is correct here.
        dosen = None

    if request.method == 'POST':
        # Pass request.FILES to the form constructor for file uploads
        form = DosenInitialProfileForm(
            request.POST, request.FILES, instance=dosen)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.initial_profile_completed = True  # Explicitly set this flag
            profile.save()  # This will save all fields, including the photo

            # Call dummy course generation if needed (as in your original code)
            if not profile.dummy_courses_generated:
                generate_dummy_courses(profile)

            messages.success(request, 'Profil berhasil disimpan')
            # Or 'dosen:dosen_home' if more appropriate
            return redirect('home')
        else:
            # If form is not valid, errors will be displayed in the template
            messages.error(request, 'Harap perbaiki kesalahan di bawah ini.')
    else:
        form = DosenInitialProfileForm(instance=dosen)

    return render(request, 'dosen/complete_initial_profile.html', {'form': form})


def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})
