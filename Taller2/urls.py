from django.urls import path
from . import views

urlpatterns = [
    path('', views.Taller2, name='Taller2'),
]
