from django import forms
from .models import PerfilUser
from portal.models import Comuna, Region
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from portal.forms import RegionComunaFormMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


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


###########################################################################
### FORM EDITAR PERFIL ###
###########################################################################


class ProfileUpdateForm(UserChangeForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Región",
        widget=forms.Select(attrs={
            "class": "form-select",
            "hx-get": "/cargar-comunas-ajax/",
            "hx-target": "#id_comuna",
            "hx-trigger": "change"
        })
    )

    # Campos de contraseña extra
    old_password = forms.CharField(
        label="Contraseña actual",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label="Repite nueva contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = PerfilUser
        fields = ["username", "first_name", "last_name", "email", "direccion", "comuna", "foto_perfil"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.comuna:
            self.fields['region'].initial = self.instance.comuna.region

    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        # Primero verificamos unicidad
        if PerfilUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya está en uso.")


        validator = UnicodeUsernameValidator()
        try:
            validator(username)
        except ValidationError:
            raise forms.ValidationError(
                "Nombre de usuario inválido. Solo puede contener letras, números y @/./+/-/_"
            )
        
        return username