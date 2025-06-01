from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MataKuliah, KelasWajib, KelasPilihan, Tugas, Materi, Absensi, PengumpulanTugas
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import KelasWajibForm, KelasPilihanForm
from django.views.decorators.http import require_POST

# Views untuk Mahasiswa
@login_required
def list_matakuliah_mahasiswa(request):
    semua_kelas_wajib = KelasWajib.objects.all()
    semua_kelas_pilihan = KelasPilihan.objects.all()
    mata_kuliah_wajib = KelasWajib.objects.filter(mahasiswa=request.user)
    mata_kuliah_pilihan = KelasPilihan.objects.filter(mahasiswa=request.user)
    context = {
        'semua_kelas_wajib': semua_kelas_wajib,
        'semua_kelas_pilihan': semua_kelas_pilihan,
        'mata_kuliah_wajib': mata_kuliah_wajib,
        'mata_kuliah_pilihan': mata_kuliah_pilihan,
    }
    return render(request, 'matakuliah/mahasiswa/list_matakuliah.html', context)

@login_required
def detail_matakuliah_mahasiswa(request, mk_id, jenis):
    """Halaman detail mata kuliah dengan materi, absensi, dan tugas"""
    if jenis == 'wajib':
        mata_kuliah = get_object_or_404(KelasWajib, id=mk_id, mahasiswa=request.user)
    else:
        mata_kuliah = get_object_or_404(KelasPilihan, id=mk_id, mahasiswa=request.user)
    
    materi_list = mata_kuliah.jadwal()
    tugas_list = mata_kuliah.list_tugas()
    absensi_mahasiswa = Absensi.objects.filter(
        mahasiswa=request.user, 
        mata_kuliah=mata_kuliah
    ).order_by('-tanggal')
    
    context = {
        'mata_kuliah': mata_kuliah,
        'materi_list': materi_list,
        'tugas_list': tugas_list,
        'absensi_list': absensi_mahasiswa,
        'jenis': jenis,
    }
    return render(request, 'matakuliah/mahasiswa/detail_matakuliah.html', context)

@login_required
@require_POST
def upload_tugas_mahasiswa(request, tugas_id):
    """Upload tugas oleh mahasiswa"""
    tugas = get_object_or_404(Tugas, id=tugas_id)
    
    if request.FILES.get('file_jawaban'):
        pengumpulan, created = PengumpulanTugas.objects.get_or_create(
            mahasiswa=request.user,
            tugas=tugas,
            defaults={'file_jawaban': request.FILES['file_jawaban']}
        )
        
        if not created:
            pengumpulan.file_jawaban = request.FILES['file_jawaban']
            pengumpulan.tanggal_upload = timezone.now()
            pengumpulan.save()
        
        messages.success(request, 'Tugas berhasil diupload!')
    else:
        messages.error(request, 'Harap pilih file untuk diupload!')
    
    return redirect('detail_matakuliah_mahasiswa', 
                   mk_id=tugas.mata_kuliah.id, 
                   jenis='wajib' if isinstance(tugas.mata_kuliah, KelasWajib) else 'pilihan')

# Views untuk Dosen
@login_required
def catalog_kelas_dosen(request):
    print("User:", request.user)
    print("Has profile:", hasattr(request.user, 'userprofile'))
    if hasattr(request.user, 'userprofile'):
        print("Role:", request.user.userprofile.role)

    if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'dosen':
        kelas_wajib = KelasWajib.objects.filter(dosen=request.user)
        kelas_pilihan = KelasPilihan.objects.filter(dosen=request.user)
        context = {
            'kelas_wajib': kelas_wajib,
            'kelas_pilihan': kelas_pilihan,
        }
        return render(request, 'matakuliah/dosen/catalog_kelas.html', context)
    else:
        messages.error(request, 'Anda tidak memiliki akses sebagai dosen.')
        return redirect('home')

@login_required
def kelola_matakuliah_dosen(request, mk_id, jenis):
    """Halaman kelola mata kuliah untuk dosen"""
    if jenis == 'wajib':
        mata_kuliah = get_object_or_404(KelasWajib, id=mk_id, dosen=request.user)
    else:
        mata_kuliah = get_object_or_404(KelasPilihan, id=mk_id, dosen=request.user)
    
    materi_list = mata_kuliah.jadwal()
    tugas_list = mata_kuliah.list_tugas()
    mahasiswa_list = mata_kuliah.mahasiswa.all()
    
    context = {
        'mata_kuliah': mata_kuliah,
        'materi_list': materi_list,
        'tugas_list': tugas_list,
        'mahasiswa_list': mahasiswa_list,
        'jenis': jenis,
    }
    return render(request, 'matakuliah/dosen/kelola_matakuliah.html', context)

@login_required
@require_POST
def tambah_materi(request, mk_id, jenis):
    """Tambah materi baru"""
    if jenis == 'wajib':
        mata_kuliah = get_object_or_404(KelasWajib, id=mk_id, dosen=request.user)
    else:
        mata_kuliah = get_object_or_404(KelasPilihan, id=mk_id, dosen=request.user)
    
    pertemuan_ke = request.POST.get('pertemuan_ke')
    judul = request.POST.get('judul')
    ringkasan = request.POST.get('ringkasan')
    tanggal = request.POST.get('tanggal')
    
    if all([pertemuan_ke, judul, ringkasan, tanggal]):
        Materi.objects.create(
            pertemuan_ke=pertemuan_ke,
            judul=judul,
            ringkasan=ringkasan,
            tanggal=tanggal,
            mata_kuliah=mata_kuliah
        )
        messages.success(request, 'Materi berhasil ditambahkan!')
    else:
        messages.error(request, 'Semua field harus diisi!')
    
    return redirect('matakuliah:kelola_matakuliah_dosen', mk_id=mk_id, jenis=jenis)

@login_required
@require_POST
def tambah_tugas_dosen(request, mk_id, jenis):
    """Tambah tugas baru oleh dosen"""
    if jenis == 'wajib':
        mata_kuliah = get_object_or_404(KelasWajib, id=mk_id, dosen=request.user)
    else:
        mata_kuliah = get_object_or_404(KelasPilihan, id=mk_id, dosen=request.user)
    
    judul = request.POST.get('judul')
    deskripsi = request.POST.get('deskripsi')
    tenggat = request.POST.get('tenggat')
    
    if all([judul, deskripsi, tenggat]):
        mata_kuliah.tambah_tugas(judul, deskripsi, tenggat)
        messages.success(request, 'Tugas berhasil ditambahkan!')
    else:
        messages.error(request, 'Semua field harus diisi!')
    
    return redirect('kelola_matakuliah_dosen', mk_id=mk_id, jenis=jenis)

@login_required
def nilai_tugas_dosen(request, tugas_id):
    """Halaman untuk menilai tugas mahasiswa"""
    tugas = get_object_or_404(Tugas, id=tugas_id, mata_kuliah__dosen=request.user)
    pengumpulan_list = PengumpulanTugas.objects.filter(tugas=tugas)
    
    if request.method == 'POST':
        pengumpulan_id = request.POST.get('pengumpulan_id')
        nilai = request.POST.get('nilai')
        feedback = request.POST.get('feedback')
        
        pengumpulan = get_object_or_404(PengumpulanTugas, id=pengumpulan_id)
        pengumpulan.nilai = nilai
        pengumpulan.feedback = feedback
        pengumpulan.save()
        
        messages.success(request, 'Nilai berhasil disimpan!')
        return redirect('nilai_tugas_dosen', tugas_id=tugas_id)
    
    context = {
        'tugas': tugas,
        'pengumpulan_list': pengumpulan_list,
    }
    return render(request, 'matakuliah/dosen/nilai_tugas.html', context)

@login_required
def absensi_mahasiswa(request, mk_id, jenis):
    """Halaman absensi untuk mahasiswa"""
    if jenis == 'wajib':
        mata_kuliah = get_object_or_404(KelasWajib, id=mk_id)
    else:
        mata_kuliah = get_object_or_404(KelasPilihan, id=mk_id)
    
    if request.method == 'POST':
        tanggal = timezone.now().date()
        absensi, created = Absensi.objects.get_or_create(
            mahasiswa=request.user,
            mata_kuliah=mata_kuliah,
            tanggal=tanggal,
            defaults={'status': 'hadir'}
        )
        
        if created:
            messages.success(request, 'Absensi berhasil dicatat!')
        else:
            messages.info(request, 'Anda sudah melakukan absensi hari ini.')
    
    return redirect('detail_matakuliah_mahasiswa', mk_id=mk_id, jenis=jenis)

@login_required
def daftar_kelas(request, kelas_id):
    """Mahasiswa mendaftar ke kelas wajib"""
    kelas = get_object_or_404(KelasWajib, id=kelas_id)
    user = request.user
    if kelas.mahasiswa.filter(id=user.id).exists():
        messages.info(request, "Anda sudah terdaftar di kelas ini.")
    else:
        kelas.mahasiswa.add(user)
        messages.success(request, "Berhasil mendaftar ke kelas.")
    # Redirect ke halaman detail kelas wajib
    return redirect('matakuliah:detail_matakuliah_mahasiswa', mk_id=kelas.id, jenis='wajib')

@login_required
def daftar_kelas_pilihan(request, kelas_id):
    """Mahasiswa mendaftar ke kelas pilihan"""
    kelas = get_object_or_404(KelasPilihan, id=kelas_id)
    user = request.user
    if kelas.mahasiswa.filter(id=user.id).exists():
        messages.info(request, "Anda sudah terdaftar di kelas ini.")
    else:
        kelas.mahasiswa.add(user)
        messages.success(request, "Berhasil mendaftar ke kelas pilihan.")
    # Redirect ke halaman detail kelas pilihan
    return redirect('matakuliah:detail_matakuliah_mahasiswa', mk_id=kelas.id, jenis='pilihan')

@login_required
def tambah_kelas(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'dosen':
        messages.error(request, 'Hanya dosen yang dapat menambah kelas.')
        return redirect('home')

    form_type = 'wajib'
    if request.method == 'POST':
        jenis = request.POST.get('jenis')
        if jenis == 'wajib':
            form = KelasWajibForm(request.POST)
            form_type = 'wajib'
            if form.is_valid():
                kelas = form.save(commit=False)
                kelas.dosen = request.user
                kelas.save()
                form.save_m2m()
                messages.success(request, 'Kelas wajib berhasil ditambahkan!')
                return redirect('matakuliah:catalog_kelas_dosen')
        else:
            form = KelasPilihanForm(request.POST)
            form_type = 'pilihan'
            if form.is_valid():
                kelas = form.save(commit=False)
                kelas.dosen = request.user
                kelas.save()
                form.save_m2m()
                messages.success(request, 'Kelas pilihan berhasil ditambahkan!')
                return redirect('matakuliah:catalog_kelas_dosen')
    else:
        form = KelasWajibForm()
        form_type = 'wajib'
    return render(request, 'matakuliah/dosen/tambah_kelas.html', {'form': form, 'form_type': form_type})
