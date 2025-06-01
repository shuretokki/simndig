from django import forms
from datadiri.models import Dosen

class DosenProfileForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = ['nama', 'nip', 'email', 'status', 'tanggal_mulai_kerja']

    def clean_nim(self):
        nim = self.cleaned_data['nim']
        qs = Dosen.objects.filter(nim=nim)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("NIP sudah terdaftar, silakan gunakan NIM lain.")
        return nim
