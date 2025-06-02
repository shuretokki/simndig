from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompleteMahasiswa
from datadiri.models import Mahasiswa
# Assuming MataKuliah is needed for 'daftar_kelas'
from matakuliah.models import MataKuliah
from django.contrib import messages


@login_required
def mahasiswa_home(request):
    try:
        mahasiswa = Mahasiswa.objects.select_related(
            'user').get(user=request.user)  # Optimized query
        if not mahasiswa.initial_profile_completed:
            messages.info(
                request, 'Mohon lengkapi profil Anda untuk melanjutkan.')
            return redirect('mahasiswa:complete_profile')
    except Mahasiswa.DoesNotExist:
        messages.warning(
            request, 'Profil mahasiswa Anda belum ada. Silakan lengkapi data diri Anda.')
        return redirect('mahasiswa:complete_profile')

    # Example: Fetch courses the student is enrolled in
    # This assumes your MataKuliah model has a ManyToManyField to User or Mahasiswa named 'mahasiswa'
    enrolled_courses = MataKuliah.objects.filter(mahasiswa=request.user)

    context = {
        'mahasiswa_profile': mahasiswa,
        'daftar_kelas': enrolled_courses,  # Renamed for clarity
        # Add other context data like announcements, tasks if available
    }
    return render(request, 'mahasiswa/home.html', context)


@login_required
def complete_profile(request):
    # Try to get the Mahasiswa instance linked to the logged-in user
    # If dosen argument is not provided, instance will be None
    # mahasiswa, created = Mahasiswa.objects.get_or_create(user=request.user)
    # The above line might prematurely create a Mahasiswa object.
    # Better to fetch or set to None for the form.
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        # If profile is already completed, optionally redirect or allow editing
        # Prevent re-completing if already done, unless editing
        if mahasiswa.initial_profile_completed and request.method == 'GET':
            # messages.info(request, "Profil Anda sudah lengkap. Anda dapat mengeditnya di sini.")
            pass  # Allow editing
    except Mahasiswa.DoesNotExist:
        mahasiswa = None  # No profile exists yet

    if request.method == 'POST':
        # If mahasiswa is None, a new Mahasiswa instance will be created by the form
        # If mahasiswa exists, it will be updated
        form = CompleteMahasiswa(
            request.POST, request.FILES, instance=mahasiswa)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Ensure user is set, especially for new instances
            profile.initial_profile_completed = True
            profile.save()
            messages.success(request, 'Profil berhasil disimpan!')
            return redirect('mahasiswa:mahasiswa_home')
        else:
            messages.error(
                request, 'Terdapat kesalahan pada form. Mohon periksa kembali.')
    else:
        # For a GET request, if a Mahasiswa instance exists, pass it to the form.
        # If it doesn't (mahasiswa is None), an unbound form for a new Mahasiswa will be created.
        initial_data = {}
        if not mahasiswa and request.user:  # Pre-fill for new profile from User object
            initial_data['nama'] = request.user.get_full_name(
            ) or request.user.username
            initial_data['email'] = request.user.email
        form = CompleteMahasiswa(instance=mahasiswa, initial=initial_data)

    return render(request, 'mahasiswa/complete_profile.html', {'form': form})

# detail_kelas view can remain as is unless it needs specific student context not already present


@login_required
def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    # You might want to check if the student is actually enrolled in this class
    # student = get_object_or_404(Mahasiswa, user=request.user)
    # if not kelas.mahasiswa.filter(id=student.user.id).exists():
    #     messages.error(request, "Anda tidak terdaftar di kelas ini.")
    #     return redirect('mahasiswa:mahasiswa_home') # Or to course list
    return render(request, 'mahasiswa/detail_kelas.html', {'kelas': kelas})
