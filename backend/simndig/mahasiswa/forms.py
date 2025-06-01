from django import forms
from datadiri.models import Mahasiswa

class CompleteMahasiswa(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nama', 'nim', 'email', 'status', 'kelas', 'jurusan', 'angkatan']

    def clean_nim(self):
        nim = self.cleaned_data['nim']
        qs = Mahasiswa.objects.filter(nim=nim)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("NIM sudah terdaftar, silakan gunakan NIM lain.")
        return nim
