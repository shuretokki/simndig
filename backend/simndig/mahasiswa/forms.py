from django import forms
from datadiri.models import Mahasiswa


class CompleteMahasiswa(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        # Ensure all desired fields for the initial profile are here
        fields = ['nama', 'email',
                  'profile_photo']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Lengkap Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contoh@student.kampus.ac.id'}),
            # 'profile_photo' will use default FileInput, which is fine
        }

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
