from django import forms
from .models import SolicitudArriendo, Inmueble, InmuebleImagen, InmuebleDocumento, MIN_IMAGES, MAX_IMAGES, MIN_DOCUMENTS, MAX_DOCUMENTS
from django.forms import inlineformset_factory


###########################################################################

                ### FORM INMUEBLE ###

###########################################################################
class InmuebleForm(forms.ModelForm):
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
            'precio_mensual',
            'comuna',
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
