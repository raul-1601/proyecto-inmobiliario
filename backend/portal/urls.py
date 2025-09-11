from django.urls import path
from .views import *


urlpatterns = [
    path('', InmueblePublicListView.as_view(), name='home'),
    path('inmueble/<int:pk>/', inmueble_detail_view, name='inmueble_detail'),
    path('inmueble/<int:pk>/editar/', InmuebleUpdateView.as_view(), name='inmueble_update'),
    path('inmueble/<int:pk>/eliminar/', InmuebleDeleteView.as_view(), name='inmueble_delete'),
    path('crear_inmueble/', InmuebleCreateView, name='inmueble_create'),
    path('mis_inmuebles', MisInmueblesListView.as_view(), name='my_properties'),

    path('perfil/', profile_view, name='profile'),

    path('solicitudes/crear/<int:inmueble_id>/', SolicitudArriendoCreateView, name='solicitud_create'),
    path('solicitudes_arrendador/', SolicitudesArrendadorListView.as_view(), name='solicitudes_arrendador'),
    path('solicitud_eliminar/<int:pk>/', SolicitudArriendoDeleteView.as_view(), name='solicitud_delete'),
    path('actualizar_solicitud/<int:pk>/', SolicitudArriendoUpdateView.as_view(), name='solicitud_update'),
    path('gestionar_solicitud/<int:pk>/', solicitud_update_arrendador_view, name='solicitud_manage'),
    path('finalizar_arriendo/<int:pk>/', finalizar_arriendo_view, name='arriendo_cancel'),

    path("ajax/cargar-comunas/", cargar_comunas_ajax, name="cargar_comunas_ajax"),
]

