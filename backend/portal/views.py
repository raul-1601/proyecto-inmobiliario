from django.shortcuts import render
""" 
from .models import Region, Comuna, SolicitudArriendo, PerfilUser, Inmueble
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .forms import RegionForm
from django.urls import reverse_lazy

# Create your views here.


class RegionListView(ListView):
    model = Region
    template_name = 'inmueble/region_list.html'
    context_object_name = 'regiones'

class RegionCreateView(CreateView):
    model = Region
    form_class = RegionForm
    template_name = 'inmueble/region_form.html'
    success_url = reverse_lazy('region_list')

class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'inmueble/region_form.html'
    success_url = reverse_lazy('region_list')

class RegionDeleteView(DeleteView):
    pass """