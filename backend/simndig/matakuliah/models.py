from django.db import models
from django.contrib.auth.models import User
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError

class Nilai(models.Model):
    tugas = models.CharField(max_length=200)
    nilai = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tugas}: {self.nilai}"

class Tugas(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    tenggat = models.DateTimeField()
    file_tugas = models.FileField(upload_to='tugas/', null=True, blank=True)
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.judul

class Materi(models.Model):
    pertemuan_ke = models.IntegerField()
    judul = models.CharField(max_length=200)
    ringkasan = models.TextField()
    tanggal = models.DateTimeField()
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Pertemuan {self.pertemuan_ke}: {self.judul}"

class Absensi(models.Model):
    mahasiswa = models.ForeignKey(User, on_delete=models.CASCADE)
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    tanggal = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('hadir', 'Hadir'),
        ('tidak_hadir', 'Tidak Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit')
    ])
    
    class Meta:
        unique_together = ['mahasiswa', 'mata_kuliah', 'tanggal']

# Abstract Base Class
class MataKuliah(models.Model):
    # Properties sesuai requirements
    _nama = models.CharField(max_length=200)  # private nama
    _nim = models.CharField(max_length=20)    # private nim  
    email = models.EmailField()               # public email
    dosen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mata_kuliah_diajar')
    mahasiswa = models.ManyToManyField(User, related_name='mata_kuliah_diambil')
    kode_mk = models.CharField(max_length=10, unique=True)
    sks = models.IntegerField()
    semester = models.IntegerField()
    
    class Meta:
        abstract = False
    
    # Getter dan Setter untuk private properties
    @property
    def nama(self):
        return self._nama
    
    @nama.setter
    def nama(self, value):
        self._nama = value
    
    @property
    def nim(self):
        return self._nim
    
    @nim.setter
    def nim(self, value):
        self._nim = value
    
    # Public methods
    def tambah_tugas(self, judul, deskripsi, tenggat):
        """Public method untuk menambah tugas"""
        tugas = Tugas.objects.create(
            judul=judul,
            deskripsi=deskripsi,
            tenggat=tenggat,
            mata_kuliah=self
        )
        return tugas
    
    def upload_tugas(self, mahasiswa, tugas_id, file):
        """Public method untuk upload tugas"""
        # Implementation for file upload
        pass
    
    def list_tugas(self):
        """Public method untuk list tugas"""
        return self.tugas_set.all()
    
    def _nilai_tugas(self, tugas_id, mahasiswa_id):
        """Protected method untuk menilai tugas"""
        # Implementation for grading
        pass
    
    def jadwal(self):
        """Public method untuk jadwal"""
        return self.materi_set.all().order_by('tanggal')
    
    def izin(self, mahasiswa, tanggal, alasan):
        """Public method untuk izin"""
        absensi, created = Absensi.objects.get_or_create(
            mahasiswa=mahasiswa,
            mata_kuliah=self,
            tanggal=tanggal,
            defaults={'status': 'izin'}
        )
        return absensi
    
    def materi(self, ke):
        """Public method untuk mengambil materi pertemuan ke-X"""
        try:
            return self.materi_set.get(pertemuan_ke=ke)
        except Materi.DoesNotExist:
            return None
    
    def __str__(self):
        return self._nama

class KelasWajib(MataKuliah):
    # Properties khusus kelas wajib
    #_nama = models.CharField(max_length=200)
    #_nim = models.CharField(max_length=20)
    nilai = models.IntegerField(default=0)
    presensi = models.IntegerField(default=0)
    
    is_wajib = models.BooleanField(default=True)
    prasyarat = models.ManyToManyField('self', blank=True)
    
    class Meta:
        verbose_name = "Kelas Wajib"
        verbose_name_plural = "Kelas Wajib"

class KelasPilihan(MataKuliah):
    # Properties khusus kelas pilihan
    #_nama = models.CharField(max_length=200)
    #_nim = models.CharField(max_length=20)
    nilai = models.IntegerField(default=0)
    presensi = models.IntegerField(default=0)
    
    is_pilihan = models.BooleanField(default=True)
    kuota_mahasiswa = models.IntegerField(default=40)
    minimal_peserta = models.IntegerField(default=10)
    
    class Meta:
        verbose_name = "Kelas Pilihan"
        verbose_name_plural = "Kelas Pilihan"

class PengumpulanTugas(models.Model):
    mahasiswa = models.ForeignKey(User, on_delete=models.CASCADE)
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
    file_jawaban = models.FileField(upload_to='jawaban_tugas/')
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    nilai = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['mahasiswa', 'tugas']
