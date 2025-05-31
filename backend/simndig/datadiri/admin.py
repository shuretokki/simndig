# datadiri/admin.py
from django.contrib import admin
from .models import Mahasiswa, Dosen, Atmin  # Import from datadiri.models

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nim', 'kelas')

@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email')

@admin.register(Atmin)
class AtminAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email')
