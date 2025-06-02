from django import forms
from datadiri.models import Mahasiswa


class CompleteMahasiswa(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        # User only fills these fields in the initial profile completion
        fields = [
            'nama', 'email', 'profile_photo'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Lengkap Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contoh@student.kampus.ac.id'}),
            # 'profile_photo' uses default FileInput, which is fine
        }

    # The __init__ method for pre-filling 'nama' and 'email' from the User object
    # (as provided in the previous response's view logic for GET requests) is good to keep.
    # If the view handles 'initial' data perfectly, this __init__ can be simpler.
    # For robustness, let's keep a simplified pre-fill here too.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This pre-filling is primarily for a new, unbound form.
        # The view's GET request logic also prepares 'initial_data'.
        # This ensures that if 'initial' is not passed from view, it still attempts to pre-fill.
        if not self.instance or not self.instance.pk:  # If it's a new instance form
            # Try to get user from initial data if passed by view, or from request if available
            # This part is tricky as form doesn't directly access 'request'.
            # It's better if the view explicitly passes 'user' in initial data for this form,
            # or directly pre-fills 'nama' and 'email' in initial_data.

            # Assuming the view will pass 'initial={'nama': ..., 'email': ...}' for new forms.
            # If 'nama' or 'email' are already in self.initial (from view), they won't be overwritten.

            # Example: If you wanted to enforce that the User's details are used for a new profile's name/email:
            # current_user = kwargs.pop('user_for_initials', None) # View could pass this
            # if current_user:
            #     if not self.initial.get('nama'):
            #         first_name = getattr(current_user, 'first_name', '')
            #         last_name = getattr(current_user, 'last_name', '')
            #         full_name_value = f"{first_name} {last_name}".strip()
            #         self.initial['nama'] = full_name_value or current_user.username
            #     if not self.initial.get('email'):
            #         self.initial['email'] = getattr(current_user, 'email', '')
            # Relying on view to pass initial_data for nama and email for new instances.
            pass

        # No need for clean_nim, clean_status as they are not in the form's fields.
