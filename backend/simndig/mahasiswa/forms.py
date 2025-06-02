from django import forms
from datadiri.models import Mahasiswa


class CompleteMahasiswa(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        # Ensure all desired fields for the initial profile are here
        fields = ['nama', 'nim', 'email', 'status',
                  'kelas', 'jurusan', 'angkatan', 'profile_photo']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Lengkap Anda'}),
            'nim': forms.TextInput(attrs={'placeholder': 'Nomor Induk Mahasiswa'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contoh@student.kampus.ac.id'}),
            'status': forms.TextInput(attrs={'placeholder': 'Contoh: Aktif, Cuti'}),
            'kelas': forms.TextInput(attrs={'placeholder': 'Contoh: TI-2A'}),
            'jurusan': forms.TextInput(attrs={'placeholder': 'Contoh: Teknik Informatika'}),
            'angkatan': forms.NumberInput(attrs={'placeholder': 'Contoh: 2022'}),
            # 'profile_photo' will use default FileInput, which is fine
        }

    def clean_nim(self):
        nim = self.cleaned_data.get('nim')
        if nim:  # Proceed only if nim is provided
            qs = Mahasiswa.objects.filter(nim=nim)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(
                    "NIM sudah terdaftar, silakan gunakan NIM lain.")
        return nim

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill name and email from user object if instance is new and these fields are empty
        # Check if user is available and has method
        if not self.instance.pk and hasattr(self.initial.get('user'), 'get_full_name'):
            user = self.initial.get('user')
            if user:
                if not self.initial.get('nama'):
                    full_name = user.get_full_name()
                    self.initial['nama'] = full_name or user.username
                if not self.initial.get('email'):
                    self.initial['email'] = user.email
        # Or, if editing and some fields are derived from User model (ensure consistency)
        elif self.instance.pk and self.instance.user:
            if not self.initial.get('nama') and not self.instance.nama:
                full_name = self.instance.user.get_full_name()
                self.initial['nama'] = full_name or self.instance.user.username
            if not self.initial.get('email') and not self.instance.email:
                self.initial['email'] = self.instance.user.email
