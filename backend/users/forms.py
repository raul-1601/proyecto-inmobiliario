from django import forms
from .models import PerfilUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from portal.forms import RegionComunaFormMixin


### FORMULARIO DE REGISTRO ###

class RegisterForm(RegionComunaFormMixin, UserCreationForm):
    class Meta:
        model = PerfilUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "direccion",
            "region",
            "comuna",
            "rut",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

### FORMULARIO DE LOGIN ### 

class LoginForm(AuthenticationForm):
    username = None  
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()   
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            user_obj = PerfilUser.objects.get(email=email)
        except PerfilUser.DoesNotExist:
            raise forms.ValidationError("Correo o contraseña inválidos.")

        self.user_cache = authenticate(self.request, username=user_obj.username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Correo o contraseña inválidos.")

        return cleaned_data

 