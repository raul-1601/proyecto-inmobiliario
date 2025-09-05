from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PerfilUser

# Register your models here.

@admin.register(PerfilUser)
class PerfilUserAdmin(UserAdmin):  ## hereda de User Admin 
    pass
    
    
    
    
    """     fieldsets = UserAdmin.fieldsets + (
        ("Información extra", {"fields": ("rut", "tipo_usuario")}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("rut", "tipo_usuario")}),
        ) """