from django.db import models

# Create your models here.

class Agro(models.Model):
    CATEGORY_CHOICES = [
        ('frutas', 'Frutas'),
        ('semillas', 'Semillas'),
        ('vegetales','Vegetales'),
    ]
    UNIT_CHOICES = [
        ('kilogramo', 'Kilogramo'),
        ('gramos', 'Gramos'),
        ('unidades','Unidades'),
    ]
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    imagen = models.ImageField(upload_to='Agro/images/')
    url = models.URLField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=15, choices=UNIT_CHOICES)
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    
    def __str__(self):
        return self.title