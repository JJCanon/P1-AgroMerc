from django.urls import path
from .views import proveedores_view

urlpatterns = [
    path('', proveedores_view, name='proveedores'),
]
