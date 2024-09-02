import csv
from django.shortcuts import render
from .models import Proveedor

def cargar_proveedores():
    with open('data/proveedores.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Proveedor.objects.update_or_create(
                nombre_proveedor=row['Nombre_Proveedor'],
                defaults={'productos': row['Productos']}
            )

def proveedores_view(request):
    cargar_proveedores()
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedores.html', {'proveedores': proveedores})
