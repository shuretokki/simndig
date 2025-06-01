from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datadiri.models import Dosen  # Corrected: Import Dosen from datadiri app
from .forms import DosenProfileForm
from matakuliah.models import MataKuliah  # Use the simplified MataKuliah model
import random  # For dummy data


@login_required
def dosen_home(request):
    try:
        # Ensure Dosen profile from datadiri.models exists
        dosen_profile = Dosen.objects.get(user=request.user)
    except Dosen.DoesNotExist:
        # If Dosen profile in datadiri.models doesn't exist,
        # try to check UserProfile role and redirect to complete_profile.
        # This relies on the UserProfile being set correctly during registration.
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'dosen':
            messages.info(request, "Please complete your Dosen profile.")
            return redirect('dosen:complete_profile')
        else:
            # Not a Dosen or UserProfile issue, redirect to main home or error page
            messages.error(
                request, "Dosen profile not found or user role is incorrect.")
            return redirect('home')  # Or an appropriate error page

    # Fetch real courses taught by the dosen
    # The 'dosen' field in MataKuliah model links to a User instance.
    courses_taught_real = MataKuliah.objects.filter(dosen=request.user)

    # Generate dummy content if no real courses or for demonstration
    dummy_courses_display = []
    is_dummy = False
    if not courses_taught_real:  # Or use `if True:` to always show dummy for testing
        is_dummy = True
        for i in range(random.randint(2, 4)):
            dummy_courses_display.append({
                'id': 0,  # Dummy id, links might not work or should be disabled
                'nama': f'Kelas {i+1} - {random.choice(["Sistem Orgasme", "Struktur Baka", "Segs", "Gooning"])}',
                'kode_mk': f'{random.randint(100000, 500000)}',
                'sks': random.randint(2, 4),
                'semester': random.randint(1, 4),
            })

    # Dummy upcoming tasks
    dummy_tasks = []
    if not courses_taught_real:  # Or always show dummy tasks
        for i in range(random.randint(1, 2)):
            dummy_tasks.append({
                'title': f'Upcoming Task {i+1}: Review Submissions',
                'due_date': 'N/A'
            })

    context = {
        'dosen_profile': dosen_profile,
        'courses_taught': courses_taught_real if courses_taught_real else dummy_courses_display,
        'is_dummy_data': is_dummy,
        'upcoming_tasks': dummy_tasks  # Add real tasks if you have a model for them
    }
    return render(request, 'dosen/home.html', context)


def detail_kelas(request, kelas_id):  # This view was also in dosen/models.py
    # Assuming kelas_id refers to MataKuliah id
    kelas = get_object_or_404(MataKuliah, id=kelas_id)
    # Add more context if needed, e.g., materi_list, tugas_list from the mata_kuliah instance
    return render(request, 'dosen/detail_kelas.html', {'kelas': kelas})


@login_required
def complete_profile(request):
    # This view creates/updates the Dosen instance in datadiri.models
    dosen_instance, created = Dosen.objects.get_or_create(
        user=request.user,
        defaults={  # Provide sensible defaults for required fields in datadiri.Dosen
            'nama': request.user.get_full_name() or request.user.username,
            # Ensure email is present
            'email': getattr(request.user, 'email', f'{request.user.username}@example.com'),
            # Dosen model in datadiri has 'nim', which is unusual for a lecturer. Adjust as needed.
            'nim': f'NIM-{request.user.id}',
            'status': 'Aktif'  # Default status
        }
    )
    if created:
        messages.info(
            request, "Your Dosen profile has been initiated. Please complete the details.")

    if request.method == 'POST':
        form = DosenProfileForm(request.POST, instance=dosen_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Ensure user is set
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dosen:dosen_home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DosenProfileForm(instance=dosen_instance)

    return render(request, 'dosen/complete_profile.html', {'form': form})
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
        form = DosenProfileForm(request.POST, instance=dosen)
        if form.is_valid():
            dosen = form.save(commit=False)
            dosen.user = request.user
            dosen.save()
            return redirect('dosen:dosen_home')
        else:
            # Form tidak valid, error akan ditampilkan di template
            pass
    else:
        form = DosenProfileForm(instance=dosen)

    return render(request, 'dosen/complete_profile.html', {'form': form})
