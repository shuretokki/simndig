from django.db import models
from django.contrib.auth.models import User
from matakuliah.models import MataKuliah

# Create your models here.
class Dosen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dosen_profile')
    nip = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def kelas(self):
        """
        Returns mata kuliah taught by this dosen's user
        To be used as: dosen.kelas.list_dosen.all()
        """
        return MataKuliah.objects.filter(dosen=self.user)
