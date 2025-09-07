from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PerfilUser(AbstractUser):
    rut = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    comuna = models.ForeignKey('portal.Comuna', on_delete=models.SET_NULL, null=True, blank=True)

    REQUIRED_FIELDS = ['rut', 'email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_username()} | {self.rut}"