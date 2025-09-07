from django.urls import path
from .views import *


urlpatterns = [
    path('', InmueblePublicListView.as_view(), name='home'),
    path('inmueble/<int:pk>/', InmuebleDetailView.as_view(), name='inmueble_detail'),
    path('inmueble/<int:pk>/editar/', InmuebleUpdateView.as_view(), name='inmueble_update'),
    path('inmueble/<int:pk>/eliminar/', InmuebleDeleteView.as_view(), name='inmueble_delete'),
    path('crear_inmueble/', InmuebleCreateView, name='inmueble_create'),
    path('mis_inmuebles', MisInmueblesListView.as_view(), name='my_properties'),
    path("ajax/cargar-comunas/", cargar_comunas_ajax, name="cargar_comunas_ajax"),
]

