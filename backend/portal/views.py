from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import SolicitudArriendo, Inmueble, Comuna
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView  
from .forms import InmuebleForm, SolicitudArriendoForm, InmuebleImagenFormSet, InmuebleDocumentoFormSet
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404



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
    template_name = 'profile/my_inmueble_list.html'
    context_object_name = 'mis_inmuebles'
    ordering = ["-id"]

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user).order_by("-id")
    

## VISTA DE DETALLE DE INMUEBLE 
class InmuebleDetailView(DetailView):
    model = Inmueble
    template_name = 'web/detail.html'


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
class SolicitudArriendoCreateView(LoginRequiredMixin, CreateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def form_valid(self, form):
        form.instance.arrendatario = self.request.user
        messages.success(self.request, "Solicitud creada correctamente.")
        return super().form_valid(form)


## LISTAR SOLICITUDES DE ARRIENDO (SECCION "MI PERFIL")
class SolicitudArriendoListView(LoginRequiredMixin, ListView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitud_list.html'
    context_object_name = 'solicitudes'


## ACTUALIZAR SOLICITUD DE ARRIENDO
class SolicitudArriendoUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'solicitud/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')


## ELIMINAR SOLICITUD DE ARRIENDO
class SolicitudArriendoDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudArriendo
    template_name = 'solicitud/solicitud_confirm_delete.html'
    success_url = reverse_lazy('solicitud_list')





###########################################################################

        ### VISTA AJAX PARA CARGAR COMUNAS EN FORMULARIOS ###

###########################################################################
from django.shortcuts import render
from .models import Comuna

def cargar_comunas_ajax(request):
    region_id = request.GET.get("region")
    if not region_id:
        return render(request, "partials/comuna_option.html", {"comunas": []})
    try:
        comunas = Comuna.objects.filter(region_id=region_id).order_by("nombre")
    except Exception:
        comunas = []
    return render(request, "partials/comuna_option.html", {"comunas": comunas})
