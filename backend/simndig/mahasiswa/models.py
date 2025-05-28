from django.db import models

class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

