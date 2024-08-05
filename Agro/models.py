from django.db import models

# Create your models here.

class Agro(models.Model):
    CATEGORY_CHOICES = [
        ('frutas', 'Frutas'),
        ('semillas', 'Semillas'),
        ('vegetales','Vegetales'),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    imagen = models.ImageField(upload_to='Agro/images/')
    url = models.URLField(blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    