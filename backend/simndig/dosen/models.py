from django.db import models
from django.contrib.auth.models import User
from matakuliah.models import MataKuliah

# Create your models here.
class Dosen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dosen_profile')
    nip = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def set_nip(self, new_nip):
        if len(new_nip) !=18:
            raise ValueError("NIP harus terdiri dari 18 digit")
        self.nip = new_nip

    def set_nama(self, nama_baru):
        self.user.username = nama_baru
        self.user.save()

    def set_tanggal_mulai_kerja(self, tanggal):
        self.tanggal_mulai_kerja = tanggal

    def get_lama_kerja(self):
        if self.tanggal_mulai_kerja:
            return date.today().year - self.tanggal_mulai_kerja.year
        return 0
    
    @property
    def kelas(self):
        """
        Returns mata kuliah taught by this dosen's user
        To be used as: dosen.kelas.list_dosen.all()
        """
        return MataKuliah.objects.filter(dosen=self.user)
