from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid



class Region(models.Model):

    class zonas_de_chile(models.TextChoices):
        norte = "Norte", _("Zona Norte")
        centro = "Centro", _("Zona Centro")
        sur = "Sur", _("Zona Sur")

    zona = models.CharField(max_length=10, choices=zonas_de_chile.choices, null=False, blank=False)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}  | Region: {self.nombre} | Zona: {self.zona}"
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="comunas") 

    def __str__(self):
        return f"{self.nombre} | Pertenece a la región: {self.region}"


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

    def __str__(self):
        return f"propietario: {self.propietario} | {self.nombre}"


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

