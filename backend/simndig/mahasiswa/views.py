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
    mahasiswa_instance, created = Mahasiswa.objects.get_or_create(
        user=request.user)

    if mahasiswa_instance.initial_profile_completed and not created and request.method == 'GET':
        # Profile is complete, but user is back on this page. Allow editing of displayed fields.
        messages.info(
            request, "Anda dapat mengedit detail profil Anda di sini.")
        pass

    if request.method == 'POST':
        form = CompleteMahasiswa(
            request.POST, request.FILES, instance=mahasiswa_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            is_first_completion = False
            if not profile.initial_profile_completed:  # Check current state before setting to True
                is_first_completion = True

            profile.initial_profile_completed = True  # Mark as complete now

            # Call save with the custom flag to trigger randomization if it's the first completion
            profile.save(_completing_initial_profile=is_first_completion)

            messages.success(request, 'Profil berhasil disimpan!')
            return redirect('mahasiswa:mahasiswa_home')
        else:
            messages.error(
                request, 'Terdapat kesalahan pada form. Mohon periksa kembali isian Anda.')
    else:
        initial_data = {}
        # Pre-fill 'nama' and 'email' for new/empty profiles from the User object
        if (created or not mahasiswa_instance.nama) and request.user:
            first_name = getattr(request.user, 'first_name', '')
            last_name = getattr(request.user, 'last_name', '')
            full_name_value = f"{first_name} {last_name}".strip()
            initial_data['nama'] = full_name_value or request.user.username

        if (created or not mahasiswa_instance.email) and request.user:  # Also pre-fill email
            initial_data['email'] = getattr(request.user, 'email', '')

        form = CompleteMahasiswa(
            instance=mahasiswa_instance, initial=initial_data if initial_data else None)

    return render(request, 'mahasiswa/complete_profile.html', {'form': form})


@login_required
def detail_kelas(request, kelas_id):
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    # You might want to check if the student is actually enrolled in this class
    # student = get_object_or_404(Mahasiswa, user=request.user)
    # if not kelas.mahasiswa.filter(id=student.user.id).exists():
    #     messages.error(request, "Anda tidak terdaftar di kelas ini.")
    #     return redirect('mahasiswa:mahasiswa_home') # Or to course list
    return render(request, 'mahasiswa/detail_kelas.html', {'kelas': kelas})
