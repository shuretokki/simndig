from django import forms
from datadiri.models import Dosen


class DosenInitialProfileForm(forms.ModelForm):
    class Meta:
        model = Dosen
        # The form now only includes fields for the user to edit.
        fields = [
            'nama',
            'email',
            'birth_date',
            'profile_photo'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contoh@kampus.ac.id'}),
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Lengkap Anda'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill name and email from the user object if they aren't already set
        if self.instance and self.instance.user:
            if not self.initial.get('nama'):
                full_name = self.instance.user.get_full_name()
                self.initial['nama'] = full_name or self.instance.user.username
            if not self.initial.get('email'):
                self.initial['email'] = self.instance.user.email
