from django import forms
from .models import *
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


###########################################################################
### FORM SELECT REGION-COMUNA ###
###########################################################################

class RegionComunaFormMixin(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all().order_by("nombre"),
        widget=forms.Select(attrs={
            "class": "form-select",
            "hx-get": reverse_lazy("cargar_comunas_ajax"),
            "hx-target": "#id_comuna",
            "hx-trigger": "change"
        }),
        required=True,
        label="Región",
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        label="Comuna",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(region_id=region_id).order_by("nombre")
            except (ValueError, TypeError):
                self.fields["comuna"].queryset = Comuna.objects.none()
        elif getattr(self.instance, "pk", None) and getattr(self.instance, "comuna", None):
            self.fields["comuna"].queryset = Comuna.objects.filter(region=self.instance.comuna.region)
            self.fields["region"].initial = self.instance.comuna.region


###########################################################################
### FORM INMUEBLE ###
###########################################################################

class InmuebleForm(RegionComunaFormMixin, forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'nombre',
            'descripcion',
            'm2_construidos',
            'm2_totales',
            'estacionamientos',
            'habitaciones',
            'banos',
            'direccion',
            'region',
            'comuna',            
            'precio_mensual',
            'tipo_inmueble'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'style': 'resize:vertical;'
            }),
        }




###########################################################################
# FORMSETS PERSONALIZADOS PARA VALIDACION MINIMA
###########################################################################

class ImagenBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = sum(
            1 for form in self.forms 
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )
        if total_forms < MIN_IMAGES:
            raise ValidationError(f"Debes subir al menos {MIN_IMAGES} imágenes.")


class DocumentoBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = sum(
            1 for form in self.forms 
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )
        if total_forms < MIN_DOCUMENTS:
            raise ValidationError(f"Debes subir al menos {MIN_DOCUMENTS} documento que acredite que eres dueño del inmueble.")



###########################################################################
# FORMSETS INLINE CON VALIDACION
###########################################################################

InmuebleImagenFormSet = inlineformset_factory(
    Inmueble,
    InmuebleImagen,
    fields=["imagen"],
    extra=0,
    can_delete=True,
    formset=ImagenBaseFormSet,
    max_num=MAX_IMAGES,
    min_num=MIN_IMAGES,
)

InmuebleDocumentoFormSet = inlineformset_factory(
    Inmueble,
    InmuebleDocumento,
    fields=["archivo"],
    extra=0,
    can_delete=True,
    formset=DocumentoBaseFormSet,
    max_num=MAX_DOCUMENTS,
    min_num=MIN_DOCUMENTS,
)


###########################################################################
### FORM SOLICITUD DE ARRIENDO ###
###########################################################################
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['inmueble', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style':'resize:vertical;'}),
        }

class SolicitudDocumentoBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = sum(
            1 for form in self.forms if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )
        if total_forms < MIN_DOCUMENTS_SOLI:
            raise ValidationError(f"Debes subir al menos {MIN_DOCUMENTS_SOLI} documentos.")

SolicitudDocumentoFormSet = inlineformset_factory(
    SolicitudArriendo,
    SolicitudDocumento,
    fields=["archivo"],
    extra=0,
    can_delete=True,
    formset=SolicitudDocumentoBaseFormSet,
    max_num=MAX_DOCUMENTS_SOLI,
    min_num=MIN_DOCUMENTS_SOLI,
)


############################################################################

class EstadoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje','estado']  # Solo se puede modificar el estado
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }