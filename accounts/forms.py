from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios.
    Hereda de UserCreationForm y añade campos como email, first_name, last_name.
    """
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese una dirección de correo válida.")
    first_name = forms.CharField(max_length=30, required=False, help_text="Opcional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Opcional.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def clean_email(self):
        """
        Validación para asegurar que el email sea único.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")
        return email

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos básicos del usuario (nombre, apellido, email).
    No permite cambiar el username aquí para simplificar.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """
        Validación para asegurar que el email, si se cambia, no pertenezca a otro usuario.
        """
        email = self.cleaned_data.get('email')
        # self.instance es el objeto User que se está editando.
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso por otro usuario.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos del perfil del usuario.
    """
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), # Usa el widget de fecha del navegador
        required=False
    )
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website_url', 'birth_date', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            # 'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}), # Opcional, para estilizar
        }

class CustomPasswordChangeForm(AuthPasswordChangeForm):
    """
    Formulario personalizado para cambiar la contraseña.
    Podrías añadir clases CSS o modificarlo si es necesario.
    Por ahora, solo lo renombramos para consistencia.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control', 'placeholder': f'Ingrese {self.fields[fieldname].label.lower()}'}
            self.fields[fieldname].help_text = '' # Limpiar help_text por defecto si no se quiere
