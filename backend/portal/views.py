from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import SolicitudArriendo, Inmueble, InmuebleImagen, InmuebleDocumento, MIN_IMAGES, MIN_DOCUMENTS
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView  
from .forms import InmuebleForm, SolicitudArriendoForm, InmuebleImagenFormSet, InmuebleDocumentoFormSet
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction


###########################################################################

                ### CRUD INMUEBLE ###

###########################################################################


## CREAR INMUEBLE
@login_required
@login_required
def InmuebleCreateView(request):
    # Instanciamos un objeto temporal para asociar los formsets
    inmueble_temp = Inmueble(propietario=request.user)

    if request.method == "POST":
        # Formulario principal
        form = InmuebleForm(request.POST)
        
        # Formsets con prefix para identificarlos correctamente
        img_formset = InmuebleImagenFormSet(
            request.POST, request.FILES,
            instance=inmueble_temp,
            prefix='imagenes'
        )
        doc_formset = InmuebleDocumentoFormSet(
            request.POST, request.FILES,
            instance=inmueble_temp,
            prefix='documentos'
        )

        if form.is_valid() and img_formset.is_valid() and doc_formset.is_valid():
            with transaction.atomic():
                # Guardamos el inmueble principal
                inmueble = form.save(commit=False)
                inmueble.propietario = request.user
                inmueble.save()

                # Asociamos los formsets al inmueble guardado
                img_formset.instance = inmueble
                img_formset.save()

                doc_formset.instance = inmueble
                doc_formset.save()

            return redirect('my_properties')  # Cambia según tu URL de lista

    else:
        # GET: instanciamos formulario vacío
        form = InmuebleForm()

        img_formset = InmuebleImagenFormSet(
            instance=inmueble_temp,
            prefix='imagenes',
            queryset=InmuebleImagen.objects.none()
        )
        doc_formset = InmuebleDocumentoFormSet(
            instance=inmueble_temp,
            prefix='documentos',
            queryset=InmuebleDocumento.objects.none()
        )

    return render(request, "inmueble/inmueble_form.html", {
        "form": form,
        "img_formset": img_formset,
        "doc_formset": doc_formset,
    })

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




