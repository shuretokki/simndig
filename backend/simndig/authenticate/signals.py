from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from datadiri.models import Dosen
from django.contrib.auth.models import User

@receiver(post_save, sender=UserProfile)
def create_role_profile(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        role = instance.role.lower()

        if role == 'dosen':
            # Buat profil Dosen jika belum ada
            Dosen.objects.get_or_create(user=user, defaults={'nama': user.username})
        # Jika mau, bisa tambah logika buat Mahasiswa, Atmin juga