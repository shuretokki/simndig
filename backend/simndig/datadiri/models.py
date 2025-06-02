from datetime import date
from django.conf import settings
from django.db import models
# Ensure you are using the correct User model (default or custom)
# from django.contrib.auth.models import User # If using default
from django.contrib.auth import get_user_model
User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=50)  # This field will be randomized

    def __str__(self):
        return f"{self.nama} ({self.user.username})"

    class Meta:
        abstract = True

    def get_nama(self):
        return self.nama

    def get_email(self):
        return self.email

    def get_status(self):
        return self.status


class Mahasiswa(Student):
    nim = models.CharField(max_length=20, unique=True)  # Will be randomized
    kelas = models.CharField(max_length=50, blank=True,
                             null=True)  # Will be randomized
    semester = models.PositiveIntegerField(
        blank=True, null=True)  # Auto-calculated
    ipk = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    ukt = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    dpa = models.CharField(max_length=100, blank=True, null=True)
    angkatan = models.PositiveIntegerField(
        blank=True, null=True)  # Will be randomized
    jurusan = models.CharField(
        max_length=100, blank=True, null=True)  # Will be randomized

    profile_photo = models.ImageField(
        upload_to='mahasiswa_profile_photos/', blank=True, null=True)
    initial_profile_completed = models.BooleanField(default=False)

    def _generate_random_nim(self):
        """Generates a unique random NIM."""
        while True:
            # Example: Generate a 10-digit NIM. Adjust length/format as needed.
            nim_value = ''.join(random.choices(string.digits, k=10))
            if not Mahasiswa.objects.filter(nim=nim_value).exists():
                return nim_value

    def save(self, *args, **kwargs):
        # Custom flag passed from the view to indicate this save is part of the initial profile completion.
        is_completing_initial_profile = kwargs.pop(
            '_completing_initial_profile', False)

        if is_completing_initial_profile and not self.initial_profile_completed:
            # Randomize fields only if they are not already set (e.g., by an admin or previous step)
            if not self.nim:
                self.nim = self._generate_random_nim()

            # 'status' is on the parent 'Student' model.
            # Ensure 'status' field on 'Mahasiswa' instance (which is a 'Student' instance) is updated.
            if not self.status:  # Accesses the status field from Student
                self.status = random.choice(
                    ["Aktif", "Cuti Sementara", "Non-Aktif"])  # Example statuses

            # Check for None, as 0 could be a valid (though unlikely) angkatan
            if self.angkatan is None:
                current_year = date.today().year
                # e.g., Angkatan from last 1-5 years
                self.angkatan = random.randint(
                    current_year - 5, current_year - 1)

            if not self.jurusan:
                jurusan_list = ["Teknik Informatika", "Sistem Informasi", "Manajemen",
                                "Akuntansi", "Desain Komunikasi Visual", "Ilmu Komunikasi"]
                self.jurusan = random.choice(jurusan_list)

            if not self.kelas:
                # Generate a somewhat realistic class name based on Jurusan and Angkatan
                jur_abbr = "".join(
                    [word[0] for word in self.jurusan.split()]).upper() if self.jurusan else "XX"
                # Use last two digits of angkatan for class year indication, or a random semester indication
                year_indicator = str(self.angkatan % 100) if self.angkatan else str(
                    random.randint(1, 4))
                self.kelas = f"{jur_abbr}-{year_indicator}{random.choice(['A', 'B', 'C', 'Pagi', 'Malam'])}"

        # Auto-calculate semester if angkatan is set (existing logic)
        if self.angkatan:
            today = date.today()
            year_diff = today.year - self.angkatan
            if today.month >= 7:  # Typically, new academic year/odd semester starts around July/August
                self.semester = year_diff * 2 + 1
            else:  # Even semester
                self.semester = year_diff * 2
            if self.semester < 1:  # Ensure semester is at least 1
                self.semester = 1
            # Cap semester if needed (e.g. max 14 for S1)
            elif self.semester > 14:
                self.semester = 14

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama} ({self.nim})"


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
