from django import forms
from .models import MataKuliah


class MataKuliahForm(forms.ModelForm):
    class Meta:
        model = MataKuliah
        fields = ['_nama', 'kode_mk', 'sks', 'semester',
                  'mahasiswa']  # Add other fields as necessary
        # Use 'nama' if you prefer to expose the property directly in forms, but _nama is the field.
