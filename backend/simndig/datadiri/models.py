import string
import random
from datetime import date
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        # Use self.user.username as a fallback if self.nama is None or empty
        return f"{self.nama or self.user.username} ({self.user.username})"

    class Meta:
        abstract = True

    def get_nama(self):
        return self.nama

    def get_email(self):
        return self.email

    def get_status(self):
        return self.status


class Mahasiswa(Student):
    nim = models.CharField(max_length=20, unique=True, blank=True, null=True)
    kelas = models.CharField(max_length=50, blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)
    ipk = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    ukt = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    dpa = models.CharField(max_length=100, blank=True, null=True)
    angkatan = models.PositiveIntegerField(blank=True, null=True)
    jurusan = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='mahasiswa_profile_photos/', blank=True, null=True)
    initial_profile_completed = models.BooleanField(default=False)

    # These methods MUST be indented to be part of the Mahasiswa class
    def _generate_random_nim(self):  # Correctly indented
        while True:
            nim_value = ''.join(random.choices(string.digits, k=10))
            if not Mahasiswa.objects.filter(nim=nim_value).exists():
                return nim_value

    def save(self, *args, **kwargs):  # Correctly indented
        is_completing_initial_profile = kwargs.pop(
            '_completing_initial_profile', False)

        if is_completing_initial_profile and not self.initial_profile_completed:
            if not self.nim:
                self.nim = self._generate_random_nim()  # Call the method with self
            if not self.status:
                self.status = random.choice(
                    ["Aktif", "Cuti Sementara", "Non-Aktif"])
            if self.angkatan is None:  # Check for None, as 0 could be valid angkatan
                current_year = date.today().year
                self.angkatan = random.randint(
                    current_year - 5, current_year - 1)
            if not self.jurusan:
                jurusan_list = ["Teknik Informatika", "Sistem Informasi", "Manajemen",
                                "Akuntansi", "Desain Komunikasi Visual", "Ilmu Komunikasi"]
                self.jurusan = random.choice(jurusan_list)
            if not self.kelas:
                jur_abbr = "".join(
                    [word[0] for word in self.jurusan.split()]).upper() if self.jurusan else "XX"
                # Ensure angkatan is not None before using for year_indicator
                year_indicator_val = self.angkatan % 100 if self.angkatan is not None else random.randint(
                    1, 4)
                self.kelas = f"{jur_abbr}-{year_indicator_val}{random.choice(['A', 'B', 'C', 'Pagi', 'Malam'])}"

        if self.angkatan is not None:  # Ensure angkatan has a value
            today = date.today()
            year_diff = today.year - self.angkatan
            if today.month >= 7:  # Typically, new academic year/odd semester starts around July/August
                self.semester = year_diff * 2 + 1
            else:  # Even semester
                self.semester = year_diff * 2

            if self.semester < 1:  # Ensure semester is at least 1
                self.semester = 1
            elif self.semester > 14:  # Example cap for S1
                self.semester = 14

        # This will now call Student.save() or Model.save() correctly
        super().save(*args, **kwargs)

    def __str__(self):  # Correctly indented
        # Use self.nama or self.user.username as fallback if nama is not set
        # Use self.nim or 'N/A' as fallback if nim is not set
        return f"{self.nama or self.user.username} ({self.nim or 'N/A'})"


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
