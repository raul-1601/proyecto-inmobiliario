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
            "tipo_usuario",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # Eliminamos username
        
        # Modificar labels
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        self.fields['email'].label = "Correo electrónico"
        self.fields['direccion'].label = "Dirección"
        self.fields['rut'].label = "RUT"
        self.fields['tipo_usuario'].label = "Tipo de usuario"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"


### FORMULARIO DE LOGIN ### 

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user_obj = PerfilUser.objects.get(email=email)
            except PerfilUser.DoesNotExist:
                raise forms.ValidationError("Correo o contraseña inválidos.")
            except PerfilUser.MultipleObjectsReturned:
                raise forms.ValidationError("Existen múltiples usuarios con este correo, contacta al administrador.")

            self.user_cache = authenticate(
                self.request,
                username=user_obj.username,  # Se sigue autenticando con username interno
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError("Correo o contraseña inválidos.")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
 