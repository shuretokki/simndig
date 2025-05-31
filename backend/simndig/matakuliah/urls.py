from django.urls import path
from . import views

app_name = 'matakuliah'

urlpatterns = [
    # URLs untuk Mahasiswa
    path('mahasiswa/', views.list_matakuliah_mahasiswa, name='list_matakuliah_mahasiswa'),
    path('mahasiswa/<int:mk_id>/<str:jenis>/', views.detail_matakuliah_mahasiswa, name='detail_matakuliah_mahasiswa'),
    path('upload-tugas/<int:tugas_id>/', views.upload_tugas_mahasiswa, name='upload_tugas_mahasiswa'),
    path('absensi/<int:mk_id>/<str:jenis>/', views.absensi_mahasiswa, name='absensi_mahasiswa'),
    
    # URLs untuk Dosen
    path('dosen/', views.catalog_kelas_dosen, name='catalog_kelas_dosen'),
    path('dosen/<int:mk_id>/<str:jenis>/', views.kelola_matakuliah_dosen, name='kelola_matakuliah_dosen'),
    path('dosen/<int:mk_id>/<str:jenis>/tambah-materi/', views.tambah_materi, name='tambah_materi'),
    path('dosen/<int:mk_id>/<str:jenis>/tambah-tugas/', views.tambah_tugas_dosen, name='tambah_tugas_dosen'),
    path('dosen/nilai-tugas/<int:tugas_id>/', views.nilai_tugas_dosen, name='nilai_tugas_dosen'),
]
