from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nama} ({self.nim})"

    class Meta:
        abstract = True

    ################### Setter methods ###################
    def set_nama(self, nama):
        self.nama = nama
        self.save()

    def set_email(self, email):
        self.email = email
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    ################### Getter methods ###################
    def get_nama(self):
        return self.nama

    def get_email(self):
        return self.email

    def get_status(self):
        return self.status


class Mahasiswa(Student):
    nim = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=50)
    semester = models.PositiveIntegerField(blank=True, null=True)
    ipk = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    ukt = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    dpa = models.CharField(max_length=100, blank=True, null=True)
    angkatan = models.PositiveIntegerField()
    jurusan = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.angkatan:
            today = date.today()
            year_diff = today.year - self.angkatan
            # Hitung semester berdasarkan bulan:
            # Januari - Juli = semester genap (2*year_diff)
            # Agustus - Desember = semester ganjil (2*year_diff + 1)
            if today.month >= 8:
                self.semester = year_diff * 2 + 1
            else:
                self.semester = year_diff * 2
            if self.semester < 1:
                self.semester = 1
        super().save(*args, **kwargs)

    # Setter
    def set_nim(self, nim):
        self.nim = nim
        self.save()

    def set_kelas(self, kelas):
        self.kelas = kelas
        self.save()

    def set_angkatan(self, angkatan):
        self.angkatan = angkatan
        self.save()

    def set_jurusan(self, jurusan):
        self.jurusan = jurusan
        self.save()

    def set_dpa(self, dpa):
        self.dpa = dpa
        self.save()

    def set_semester(self, semester):
        self.semester = semester
        self.save()

    def set_ipk(self, ipk):
        self.ipk = ipk
        self.save()

    def set_ukt(self, ukt):
        self.ukt = ukt
        self.save()

    ################### Getter Methods ###################
    def get_dpa(self):
        return self.dpa

    def get_nim(self):
        return self.nim

    def get_kelas(self):
        return self.kelas

    def get_angkatan(self):
        return self.angkatan

    def get_jurusan(self):
        return self.jurusan

    def get_semester(self):
        return self.semester

    def get_ipk(self):
        return self.ipk

    def get_ukt(self):
        return self.ukt

    def ambilKelas(self):

        return ["Matematika", "Fisika", "Pemrograman", "Basis Data", "PBO"]

    def absen(self):

        return 92.5

    def KHS(self):
        return {
            "Matematika": "A",
            "Fisika": "B+",
            "Pemrograman": "A-",
            "Basis Data": "B",
        }

    def bayar_ukt(self):

        return 2500000.00

    def lunas_ukt(self):

        return self.bayar_ukt() >= self.ukt
    # field khusus mahasiswa


class Dosen(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dosen_profile')
    nama = models.CharField(max_length=255, blank=True, null=True)
    nip = models.CharField(max_length=20, unique=True,
                           blank=True, null=True)  # Filled in initial step
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    tanggal_mulai_kerja = models.DateField(
        blank=True, null=True)  # Filled in initial step
    current_semester = models.IntegerField(
        blank=True, null=True)  # Filled in initial step

    # Fields for advanced profile
    birth_date = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='dosen_profile_photos/', blank=True, null=True)

    # Flags to track profile status
    initial_profile_completed = models.BooleanField(default=False)
    dummy_courses_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.nama or self.user.username


class Atmin(Student):
    pass
