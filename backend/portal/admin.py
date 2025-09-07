from django.contrib import admin
from .models import Inmueble, InmuebleImagen, InmuebleDocumento, Comuna, Region

# -------------------------
# Inlines para Imágenes y Documentos
# -------------------------
class InmuebleImagenInline(admin.TabularInline):
    model = InmuebleImagen
    extra = 1
    readonly_fields = ('imagen_preview',)
    fields = ('imagen', 'imagen_preview')
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" style="max-height: 100px;" />'
        return "-"
    imagen_preview.allow_tags = True
    imagen_preview.short_description = "Vista previa"


class InmuebleDocumentoInline(admin.TabularInline):
    model = InmuebleDocumento
    extra = 1
    readonly_fields = ('archivo_link',)
    fields = ('archivo', 'archivo_link')
    
    def archivo_link(self, obj):
        if obj.archivo:
            return f'<a href="{obj.archivo.url}" target="_blank">{obj.archivo.name}</a>'
        return "-"
    archivo_link.allow_tags = True
    archivo_link.short_description = "Documento"


# -------------------------
# Admin de Inmueble
# -------------------------
@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 
        'propietario', 
        'tipo_inmueble', 
        'comuna', 
        'precio_mensual', 
        'arrendado', 
        'creado', 
        'actualizado'
    )
    list_filter = ('tipo_inmueble', 'arrendado', 'comuna')
    search_fields = ('nombre', 'direccion', 'propietario__username')
    readonly_fields = ('creado', 'actualizado')
    inlines = [InmuebleImagenInline, InmuebleDocumentoInline]
    ordering = ('-creado',)


# -------------------------
# Admin de Comuna y Región (opcional)
# -------------------------
@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    list_filter = ('region',)
    search_fields = ('nombre',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona')
    list_filter = ('zona',)
    search_fields = ('nombre',)
