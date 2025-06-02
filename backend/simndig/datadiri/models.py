from datetime import date
from django.conf import settings
from django.db import models
# Ensure you are using the correct User model (default or custom)
# from django.contrib.auth.models import User # If using default
from django.contrib.auth import get_user_model
User = get_user_model()


class Student(models.Model):  # This is an abstract class in your file
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    # Consider if unique=True is needed if User.email is the source
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)

    # __str__ for abstract model might be less useful unless it's overridden by children
    def __str__(self):
        return f"{self.nama} ({self.user.username})"

    class Meta:
        abstract = True

    # ... (Keep existing setter/getter methods for Student if they are still relevant) ...
    def get_nama(self):
        return self.nama

    def get_email(self):
        return self.email

    def get_status(self):
        return self.status


class Mahasiswa(Student):
    nim = models.CharField(max_length=20, unique=True)
    # Made blank/null True for flexibility
    kelas = models.CharField(max_length=50, blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)
    ipk = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    ukt = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    dpa = models.CharField(max_length=100, blank=True, null=True)
    # Made blank/null True for flexibility
    angkatan = models.PositiveIntegerField(blank=True, null=True)
    jurusan = models.CharField(
        max_length=100, blank=True, null=True)  # Made blank/null True

    # New fields for profile completion
    profile_photo = models.ImageField(
        upload_to='mahasiswa_profile_photos/', blank=True, null=True)
    initial_profile_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.angkatan:  # Ensure angkatan has a value before calculating semester
            today = date.today()
            year_diff = today.year - self.angkatan
            # August or later (typically start of odd semester)
            if today.month >= 8:
                self.semester = year_diff * 2 + 1
            else:  # January to July (typically even semester)
                self.semester = year_diff * 2
            if self.semester < 1:
                self.semester = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama} ({self.nim})"

    # ... (Keep existing setter/getter methods for Mahasiswa) ...
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

# ... (Dosen and Atmin models remain the same as in your file unless other changes are needed) ...


class Dosen(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dosen_profile')
    nama = models.CharField(max_length=255, blank=True, null=True)
    nip = models.CharField(max_length=20, unique=True,
                           blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    tanggal_mulai_kerja = models.DateField(
        blank=True, null=True)
    current_semester = models.IntegerField(
        blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='dosen_profile_photos/', blank=True, null=True)
    initial_profile_completed = models.BooleanField(default=False)
    dummy_courses_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.nama or self.user.username


class Atmin(Student):
    pass
