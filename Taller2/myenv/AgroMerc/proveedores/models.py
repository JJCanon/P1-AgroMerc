from django.db import models
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    productos = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_proveedor