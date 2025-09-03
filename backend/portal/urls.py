from django.urls import path
from .views import *


urlpatterns = [
    path('', InmueblePublicListView.as_view(), name='home'),
    path('inmueble/<int:pk>/', InmuebleDetailView.as_view(), name='inmueble_detail'),
    path('inmueble/nuevo/', InmuebleCreateView.as_view(), name='inmueble_create'),
    path('inmueble/<int:pk>/editar/', InmuebleUpdateView.as_view(), name='inmueble_update'),
    path('inmueble/<int:pk>/eliminar/', InmuebleDeleteView.as_view(), name='inmueble_delete'),
]

