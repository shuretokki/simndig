from django.contrib import admin
from .models import MataKuliah, KelasWajib, KelasPilihan, Tugas, Materi, Absensi, PengumpulanTugas, Nilai

@admin.register(KelasWajib)
class KelasWajibAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kode_mk', 'dosen', 'sks', 'semester']
    list_filter = ['semester', 'sks']
    search_fields = ['nama', 'kode_mk']
    filter_horizontal = ['mahasiswa', 'prasyarat']

@admin.register(KelasPilihan)
class KelasPilihanAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kode_mk', 'dosen', 'sks', 'semester', 'kuota_mahasiswa']
    list_filter = ['semester', 'sks']
    search_fields = ['nama', 'kode_mk']
    filter_horizontal = ['mahasiswa']

@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = ['judul', 'mata_kuliah', 'tenggat']
    list_filter = ['mata_kuliah', 'tenggat']
    search_fields = ['judul', 'mata_kuliah__nama']

@admin.register(Materi)
class MateriAdmin(admin.ModelAdmin):
    list_display = ['judul', 'mata_kuliah', 'pertemuan_ke', 'tanggal']
    list_filter = ['mata_kuliah', 'tanggal']
    search_fields = ['judul', 'mata_kuliah__nama']

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ['mahasiswa', 'mata_kuliah', 'tanggal', 'status']
    list_filter = ['status', 'tanggal', 'mata_kuliah']
    search_fields = ['mahasiswa__username', 'mata_kuliah__nama']

@admin.register(PengumpulanTugas)
class PengumpulanTugasAdmin(admin.ModelAdmin):
    list_display = ['mahasiswa', 'tugas', 'tanggal_upload', 'nilai']
    list_filter = ['tanggal_upload', 'tugas__mata_kuliah']
    search_fields = ['mahasiswa__username', 'tugas__judul']
