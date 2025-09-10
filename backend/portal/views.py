from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import password_validation
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView  
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from users.models import PerfilUser
from users.forms import ProfileUpdateForm




###########################################################################

                ### CRUD INMUEBLE ###

###########################################################################


## CREAR INMUEBLE
@login_required
def InmuebleCreateView(request):
    """Crear un nuevo inmueble con sus imágenes y documentos."""
    
    instance = Inmueble(propietario=request.user)
    
    if request.method == "POST":
        form = InmuebleForm(request.POST, instance=instance)
        img_formset = InmuebleImagenFormSet(request.POST, request.FILES, instance=instance, prefix="imagenes")
        doc_formset = InmuebleDocumentoFormSet(request.POST, request.FILES, instance=instance, prefix="documentos")

        if form.is_valid() and img_formset.is_valid() and doc_formset.is_valid():
            with transaction.atomic():
                form.save()
                img_formset.save()
                doc_formset.save()

            messages.success(request, "Inmueble creado correctamente.")
            return redirect("my_properties")
        else:
            messages.error(request, "Corrige los errores en el formulario y vuelve a enviar.")

    else:
        form = InmuebleForm(instance=instance)
        img_formset = InmuebleImagenFormSet(instance=instance, prefix="imagenes")
        doc_formset = InmuebleDocumentoFormSet(instance=instance, prefix="documentos")

    # Renderiza el formulario (POST válido o GET)
    context = {
        "form": form,
        "img_formset": img_formset,
        "doc_formset": doc_formset
    }
    return render(request, "inmueble/inmueble_form.html", context)



## LISTAR INMUEBLES (HOME)
class InmueblePublicListView(ListView):
    model = Inmueble
    template_name = 'web/home.html'
    context_object_name = 'inmuebles'


## LISTAR INMUEBLES DEL USUARIO (SECCION "MI PERFIL")
class MisInmueblesListView(LoginRequiredMixin, ListView):
    model = Inmueble
    template_name = 'profile/profile.html'
    context_object_name = 'mis_inmuebles'
    ordering = ["-id"]

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user).order_by("-id")
    

## VISTA DE DETALLE DE INMUEBLE 
class InmuebleDetailView(DetailView):
    model = Inmueble
    template_name = 'inmueble/detail.html'


## ACTUALIZAR DATOS INMUEBLE
class InmuebleUpdateView(LoginRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'inmueble/inmueble_form.html'
    success_url = reverse_lazy('inmueble_list')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)


## ELIMINAR INMUEBLE
class InmuebleDeleteView(LoginRequiredMixin, DeleteView):
    model = Inmueble
    template_name = 'inmueble/inmueble_confirm_delete.html'
    success_url = reverse_lazy('inmueble_list')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)



###########################################################################

                ### CRUD SOLICITUD ARRIENDO ###

###########################################################################
## CREAR SOLICITUD DE ARRIENDO
@login_required
def SolicitudArriendoCreateView(request, inmueble_id):
    """Crear una solicitud de arriendo con sus documentos."""

    # Creamos la instancia en memoria con los datos iniciales
    instance = SolicitudArriendo(arrendatario=request.user, inmueble_id=inmueble_id)

    if request.method == "POST":
        # Primero llenamos el formulario con POST
        form = SolicitudArriendoForm(request.POST, instance=instance)

        if form.is_valid():
            # Guardamos la solicitud principal primero, para que tenga PK
            instance = form.save(commit=False)
            instance.arrendatario = request.user
            instance.inmueble_id = inmueble_id
            instance.save()  # <-- aquí se guarda en DB y ahora tiene pk

            # Ahora sí podemos instanciar el formset con instance guardada
            doc_formset = SolicitudDocumentoFormSet(
                request.POST, request.FILES, instance=instance, prefix="documentos"
            )

            if doc_formset.is_valid():
                doc_formset.save()
                messages.success(request, "Solicitud creada correctamente.")
                return redirect("home")
            else:
                messages.error(request, "Corrige los errores en los documentos.")
        else:
            # Si el form principal no es válido, creamos un formset vacío para mostrar
            doc_formset = SolicitudDocumentoFormSet(instance=instance, prefix="documentos")
            messages.error(request, "Corrige los errores en el formulario principal.")
    else:
        form = SolicitudArriendoForm(instance=instance)
        doc_formset = SolicitudDocumentoFormSet(instance=instance, prefix="documentos")

    context = {
        "form": form,
        "doc_formset": doc_formset,
        "inmueble": instance.inmueble
    }
    return render(request, "solicitud/solicitud_form.html", context)


            

## LISTAR SOLICITUDES DE ARRIENDO (SECCION "MI PERFIL")
class SolicitudesArrendatarioListView(LoginRequiredMixin, ListView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitudes_arrendatario.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)

## LISTAR SOLICITUDES DE ARRIENDO vista del propietario (SECCION "MI PERFIL")
class SolicitudesArrendadorListView(LoginRequiredMixin, ListView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitudes_arrendador.html'
    context_object_name = 'solicitudes'
    ordering = ['-creado']

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(inmueble__propietario=self.request.user).order_by('inmueble__id', 'creado')



## ACTUALIZAR SOLICITUD DE ARRIENDO
class SolicitudArriendoUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)

## ELIMINAR SOLICITUD DE ARRIENDO
class SolicitudArriendoDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitud_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return SolicitudArriendo.objects.filter(arrendatario=self.request.user)



###########################################################################

        ### VISTA AJAX PARA CARGAR COMUNAS EN FORMULARIOS ###

###########################################################################

def cargar_comunas_ajax(request):
    region_id = request.GET.get("region")
    if not region_id:
        return render(request, "partials/comuna_option.html", {"comunas": []})
    try:
        comunas = Comuna.objects.filter(region_id=region_id).order_by("nombre")
    except Exception:
        comunas = []
    return render(request, "partials/comuna_option.html", {"comunas": comunas})




###########################################################################

@login_required
def profile_view(request):
    mis_inmuebles = None
    gestion_solicitudes = None
    mis_solicitudes = None
    tab_activo = "mi-perfil"
    form = None

    if request.user.tipo_usuario == PerfilUser.TipoUsuario.arrendador:
        mis_inmuebles = Inmueble.objects.filter(propietario=request.user).order_by("-id")
        gestion_solicitudes = SolicitudArriendo.objects.filter(inmueble__propietario=request.user).order_by('inmueble__id', 'creado')
    else:
        mis_solicitudes = SolicitudArriendo.objects.filter(arrendatario=request.user).order_by("-creado")

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            new_password1 = form.cleaned_data.get("new_password1")
            new_password2 = form.cleaned_data.get("new_password2")
            old_password = form.cleaned_data.get("old_password")
            print("---------------------formulario valido-----------------------")
            if new_password1 or new_password2 or old_password:
                if not old_password:
                    print("---------------------contraseña actual vacia-----------------------")
                    form.add_error("old_password","La contraseña actual es obligatoria para cambiar la contraseña.")
                elif not request.user.check_password(old_password):
                    form.add_error("old_password","La contraseña actual es incorrecta.")

                if not new_password1 or not new_password2:
                    form.add_error("new_password1","Ambos campos de nueva contraseña son obligatorios.")
                if new_password1 != new_password2:
                    form.add_error("new_password2", "Las nuevas contraseñas no coinciden.")

                
                if new_password1:
                    try:
                        password_validation.validate_password(new_password1, user)
                    except ValidationError as e:
                        form.add_error("new_password1", " ".join(e.messages))


                if form.errors:
                    tab_activo = "actualizar-datos"

                else:
                    user.set_password(new_password1)


            
            if not new_password1 and not new_password2 and not old_password and not form.has_changed():
                print("---------------------no se realizaron cambios-----------------------")
                messages.info(request, "No se realizaron cambios.")
                return redirect("profile")

            elif not form.errors:
                user.save()
                messages.success(request, "Perfil actualizado correctamente")
                return redirect("profile")


        else:
            tab_activo = "actualizar-datos"

    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        "user": request.user,
        "mis_inmuebles": mis_inmuebles,
        "gestion_solicitudes": gestion_solicitudes,
        "mis_solicitudes": mis_solicitudes,
        "form": form,
        "regiones": Region.objects.all(),
        "comunas": Comuna.objects.filter(region=request.user.comuna.region if request.user.comuna else None),
        "tab_activo": tab_activo,
    }
    return render(request, "profile/profile.html", context)
