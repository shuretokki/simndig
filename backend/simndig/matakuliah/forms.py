from django import forms
from .models import KelasWajib, KelasPilihan


class KelasWajibForm(forms.ModelForm):
    class Meta:
        model = KelasWajib
        fields = ['_nama', 'kode_mk', 'sks', 'semester', 'prasyarat']


class KelasPilihanForm(forms.ModelForm):
    class Meta:
        model = KelasPilihan
        fields = ['_nama', 'kode_mk', 'sks', 'semester',
                  'kuota_mahasiswa', 'minimal_peserta']
