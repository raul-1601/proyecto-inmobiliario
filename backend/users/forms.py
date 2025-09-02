from django import forms
from .models import PerfilUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


### FORMULARIO DE REGISTRO ###

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = PerfilUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "rut",
            "tipo_usuario",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields.pop('tipo_usuario', None)

### FORMULARIO DE LOGIN ### 

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="usuario@correo.cl")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)