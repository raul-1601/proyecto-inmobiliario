from django.urls import path
from .views import register_view


urlpatterns = [
    path('propietario/', lambda r: register_view(r, 'ARRENDADOR'), name='register_owner'),
    path('arrendatario/', lambda r: register_view(r, 'ARRENDATARIO'), name='register_tenant'),
]