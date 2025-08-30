""" from django import forms
from .models import Region, Comuna, SolicitudArriendo, PerfilUser, Inmueble


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['nro_region', 'nombre']
 """