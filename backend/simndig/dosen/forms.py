from django import forms
from datadiri.models import Dosen


class DosenInitialProfileForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = ['nip', 'email', 'status',
                  'tanggal_mulai_kerja', 'current_semester']
        widgets = {
            'tanggal_mulai_kerja': forms.DateInput(attrs={'type': 'date'}),
            'current_semester': forms.NumberInput(attrs={'placeholder': 'e.g., 20231 for Gasal 2023/2024'}),
        }

    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        if not nip:
            # NIP can be optional initially if desired, or raise ValidationError
            return nip
        qs = Dosen.objects.filter(nip=nip)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "NIP sudah terdaftar, silakan gunakan NIP lain.")
        return nip


class DosenAdvancedProfileForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = ['nama', 'birth_date', 'profile_photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
