from django import forms
from .models import PerfilUser
from django.forms import ModelForm
from portal.models import Comuna, Region
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


###########################################################################
### FORM EDITAR PERFIL ###
###########################################################################




class ProfileUpdateForm(forms.ModelForm):
    # Campo extra para seleccionar la región
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Región",
        widget=forms.Select(attrs={
            "class": "form-select",
            "hx-get": "/cargar-comunas-ajax/",       # tu endpoint HTMX
            "hx-target": "#id_comuna",               # el select de comuna
            "hx-trigger": "change"
        })
    )

    class Meta:
        model = PerfilUser
        fields = ["first_name", "last_name", "email", "direccion", "comuna", "foto_perfil"]
        widgets = {
            "first_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "last_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "comuna": forms.Select(attrs={"class": "form-select", "id": "id_comuna"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa el campo region según la comuna actual
        if self.instance.comuna:
            self.fields['region'].initial = self.instance.comuna.region