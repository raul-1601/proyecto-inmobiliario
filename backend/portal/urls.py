""" from django.urls import path
from .views import RegionListView, RegionCreateView, RegionUpdateView, RegionDeleteView
urlpatterns = [
    path('listar_regiones/', RegionListView.as_view(),name='region_list'),
    path('crear_regiones/', RegionCreateView.as_view(),name='region_create'),
    path('actualizar_region/<int:pk>/', RegionUpdateView.as_view(),name='region_update'),
]
 """