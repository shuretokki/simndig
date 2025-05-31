from django.shortcuts import render
from datadiri.models import Mahasiswa

def daftar_mahasiswa(request):
    semua_mahasiswa = Mahasiswa.objects.all()
# ... lanjutkan logika view
# Create your views here.
