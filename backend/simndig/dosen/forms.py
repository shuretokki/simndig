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
        user = self.instance.user  # Assign to a local variable for clarity

        if not self.initial.get('nama'):
            # Attempt to get first_name and last_name attributes.
            # Default to an empty string if the attribute is not found.
            first_name = getattr(user, 'first_name', '')
            last_name = getattr(user, 'last_name', '')

            # Construct the full name.
            # The .strip() method handles cases where one of the names is empty
            # or if both are empty (resulting in an empty string).
            constructed_name = f"{first_name} {last_name}".strip()

            # Use the constructed_name if it's not empty, otherwise fallback to the user's username.
            # It's assumed user.username exists, as per the original code's fallback.
            self.initial['nama'] = constructed_name or user.username

        if not self.initial.get('email'):
            # It's assumed user.email exists, as the original code for email did not error.
            # For added robustness, getattr(user, 'email', '') could be used.
            self.initial['email'] = user.email
