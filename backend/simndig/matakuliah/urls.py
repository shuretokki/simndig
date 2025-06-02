from django.urls import path
from . import views

app_name = 'matakuliah'

urlpatterns = [
    # Mahasiswa URLs
    path('m/', views.list_matakuliah_mahasiswa,
         name='list_matakuliah_mahasiswa'),
    path('m/<int:mk_id>/<str:jenis>/', views.detail_matakuliah_mahasiswa,
         name='detail_matakuliah_mahasiswa'),
    path('m/upload/<int:tugas_id>/', views.upload_tugas_mahasiswa,
         name='upload_tugas_mahasiswa'),
    path('m/absen/<int:mk_id>/<str:jenis>/',
         views.absensi_mahasiswa, name='absensi_mahasiswa'),
    path('daftar-kelas/<int:kelas_id>/',
         views.daftar_kelas, name='daftar_kelas'),
    path('daftar-kelas-pilihan/<int:kelas_id>/',
         views.daftar_kelas_pilihan, name='daftar_kelas_pilihan'),
    # Dosen URLs
    path('d/', views.catalog_kelas_dosen, name='catalog_kelas_dosen'),
    path('d/<int:mk_id>/<str:jenis>/', views.kelola_matakuliah_dosen,  # Added <str:jenis>
         name='kelola_matakuliah_dosen'),  # Ensure view accepts 'jenis'
    path('d/<int:mk_id>/<str:jenis>/materi/',
         views.tambah_materi, name='tambah_materi'),
    path('d/<int:mk_id>/<str:jenis>/tugas/',
         views.tambah_tugas_dosen, name='tambah_tugas_dosen'),
    path('d/nilai/<int:tugas_id>/',
         views.nilai_tugas_dosen, name='nilai_tugas_dosen'),
    path('d/tambah/', views.tambah_kelas, name='tambah_kelas'),
]
