from django.shortcuts import render
from .models import SolicitudArriendo, Inmueble
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .forms import InmuebleForm, SolicitudArriendoForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return render(request, 'web/home.html')



### CRUD INMUEBLE ###

class InmuebleCreateView(LoginRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'inmueble/inmueble_form.html'
    success_url = reverse_lazy('inmueble_list')

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)


class InmueblePublicListView(ListView):
    model = Inmueble
    template_name = 'inmueble/inmueble_list.html'
    context_object_name = 'inmuebles'


class MisInmueblesListView(LoginRequiredMixin, ListView):
    model = Inmueble
    template_name = 'inmueble/my_inmueble_list.html'
    context_object_name = 'mis_inmuebles'

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)


class InmuebleUpdateView(LoginRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'inmueble/inmueble_form.html'
    success_url = reverse_lazy('inmueble_list')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)


class InmuebleDeleteView(LoginRequiredMixin, DeleteView):
    model = Inmueble
    template_name = 'inmueble/inmueble_confirm_delete.html'
    success_url = reverse_lazy('inmueble_list')

    def get_queryset(self):
        return Inmueble.objects.filter(propietario=self.request.user)


###########################################################################

### CRUD SOLICITUD ARRIENDO ###

class SolicitudArriendoCreateView(LoginRequiredMixin, CreateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'inmueble/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')


class SolicitudArriendoListView(LoginRequiredMixin, ListView):
    model = SolicitudArriendo
    template_name = 'inmueble/solicitud_list.html'
    context_object_name = 'solicitudes'

class SolicitudArriendoUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudArriendo
    form_class = SolicitudArriendoForm
    template_name = 'inmueble/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')


class SolicitudArriendoDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudArriendo
    template_name = 'inmueble/solicitud_confirm_delete.html'
    success_url = reverse_lazy('solicitud_list')