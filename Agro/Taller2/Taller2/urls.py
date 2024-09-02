from django.urls import path
from . import views

app_name = 'Taller2'

urlpatterns = [
    path('', views.Taller2, name='Taller2'),
]
