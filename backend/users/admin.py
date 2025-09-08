from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PerfilUser
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(PerfilUser)
class PerfilUserAdmin(UserAdmin):
    model = PerfilUser

    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')

    # Campos que se pueden buscar
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut')
    ordering = ('username',)

    # Configuración de los formularios de edición y creación
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'email', 'rut', 'direccion', 'comuna', 'foto_perfil', 'tipo_usuario')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    # Para el formulario de creación de usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'rut', 'first_name', 'last_name', 'tipo_usuario', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )