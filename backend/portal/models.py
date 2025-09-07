from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid
from .validators import FileSizeValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible


###########################################################################

                ### MODELO REGION ###

###########################################################################
class Region(models.Model):

    class zonas_de_chile(models.TextChoices):
        norte = "Norte", _("Zona Norte")
        centro = "Centro", _("Zona Centro")
        sur = "Sur", _("Zona Sur")

    zona = models.CharField(max_length=10, choices=zonas_de_chile.choices, null=False, blank=False)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"Region: {self.nombre} | Zona: {self.zona}"



###########################################################################

                ### MODELO COMUNA ###

###########################################################################
class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas") 

    def __str__(self):
        return f"{self.nombre}"



###########################################################################

                ### MODELO INMUEBLE ###

###########################################################################

MIN_IMAGES = 3
MAX_IMAGES = 10
MIN_DOCUMENTS = 1
MAX_DOCUMENTS = 5

class Inmueble(models.Model):

    class TipoInmueble(models.TextChoices):
        casa = "CASA", _("Casa")
        departamento = "DEPARTAMENTO", _("Departamento")
        parcela = "PARCELA", _("Parcela")

    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inmuebles", blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(default=0)
    m2_totales = models.FloatField(default=0)
    estacionamientos = models.PositiveIntegerField(default=0)
    habitaciones = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=100)
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT)
    tipo_inmueble = models.CharField(max_length=20, choices=TipoInmueble.choices)
    arrendado = models.BooleanField(default=False)

    ## validacion de la cantidad y tamaño de imagenes y documentos
    def clean(self):
        if not self.pk:
            return
    
        total_imagenes = self.imagenes.count()
        total_documentos = self.documentos.count()

        if total_imagenes < MIN_IMAGES:
            raise ValidationError(f"Un inmueble debe tener al menos {MIN_IMAGES} imágenes.")
        if total_imagenes > MAX_IMAGES:
            raise ValidationError(f"Un inmueble no puede tener más de {MAX_IMAGES} imágenes.")

        if total_documentos < MIN_DOCUMENTS:
            raise ValidationError(f"Un inmueble debe tener al menos {MIN_DOCUMENTS} documentos.")
        if total_documentos > MAX_DOCUMENTS:
            raise ValidationError(f"Un inmueble no puede tener más de {MAX_DOCUMENTS} documentos.")





    def __str__(self):
        return f"propietario: {self.propietario} | {self.nombre}"
    


###########################################################################

                ### MODELO IMAGENES DEL INMUEBLE ###

###########################################################################
class InmuebleImagen(models.Model):
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="imagenes_inmueble")
    imagen = models.ImageField(upload_to="inmuebles/fotos/")
    
    def __str__(self):
        return f"Imagen del inmueble {self.inmueble.titulo}, propiedad de {self.inmueble.propietario}"
    


###########################################################################

                ### MODELO IMAGENES DEL INMUEBLE ###

###########################################################################
class InmuebleDocumento(models.Model):
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="documentos_inmueble")
    archivo = models.FileField(
        upload_to="inmuebles/documentos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]),
            FileSizeValidator(max_mb=10)
            ]
        )
    
    def __str__(self):
        return f"Documento del inmueble {self.inmueble.titulo}, propiedad de {self.inmueble.propietario}"
    


###########################################################################

                ### MODELO SOLICITUD DE ARRIENDO ###

###########################################################################
class SolicitudArriendo(models.Model):

    class EstadoSolicitud(models.TextChoices):
        pendiente = "PENDIENTE", _("Pendiente ⏳")
        aprobada = "APROBADA", _("Aprobada ✔️")
        rechazada = "RECHAZADA", _("Rechazada ❌")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="solicitudes")
    mensaje = models.TextField()
    arrendatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    estado = models.CharField(max_length=20, choices=EstadoSolicitud.choices, default=EstadoSolicitud.pendiente)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid} | Persona que solicita: {self.arrendatario} | Estado solicitud: {self.estado} "

