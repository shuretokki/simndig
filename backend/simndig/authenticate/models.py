# authenticate/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
        ('admin', 'Admin'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.role}"
