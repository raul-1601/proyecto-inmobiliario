from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PerfilUser(AbstractUser):

    class TipoUsuario(models.TextChoices):
        arrendatario = "ARRENDATARIO", _("Arrendatario")
        arrendador = "ARRENDADOR", _("Arrendador")

    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.arrendatario)
    rut = models.CharField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['rut', 'email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_username()} | {self.tipo_usuario}"