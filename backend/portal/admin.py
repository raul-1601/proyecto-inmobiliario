from django.contrib import admin
from .models import Comuna, Region, Inmueble, SolicitudArriendo


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'zona') 
    list_filter = ('zona',)                 
    search_fields = ('nombre',)             


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region')  
    list_filter = ('region',)                 
    search_fields = ('nombre',) 

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    pass

@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    pass


