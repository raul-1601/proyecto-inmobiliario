from django import forms
from .models import SolicitudArriendo, Inmueble, InmuebleImagen, InmuebleDocumento, Region, Comuna, MIN_IMAGES, MAX_IMAGES, MIN_DOCUMENTS, MAX_DOCUMENTS
from django.forms import inlineformset_factory
from django.urls import reverse_lazy



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

        if "region" in self.data:  # si viene del POST
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(region_id=region_id).order_by("nombre")
            except (ValueError, TypeError):
                self.fields["comuna"].queryset = Comuna.objects.none()
        elif getattr(self.instance, "pk", None) and getattr(self.instance, "comuna", None):
            # Si es edición: setear la comuna de su región
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


InmuebleImagenFormSet = inlineformset_factory(
    Inmueble,
    InmuebleImagen,
    fields=["imagen"],
    extra=1,
    can_delete=True,
    min_num=MIN_IMAGES,
    max_num=MAX_IMAGES,
    validate_min=True,
    validate_max=True,
)

InmuebleDocumentoFormSet = inlineformset_factory(
    Inmueble,
    InmuebleDocumento,
    fields=["archivo"],
    extra=1,
    can_delete=True,
    min_num=MIN_DOCUMENTS,
    max_num=MAX_DOCUMENTS,
    validate_min=True,
    validate_max=True,
)

        

###########################################################################

                ### FORM SOLICITUD DE ARRIENDO ###

###########################################################################
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['inmueble', 'mensaje']




