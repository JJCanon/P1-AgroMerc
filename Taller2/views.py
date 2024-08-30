from django.shortcuts import render
from .models import taller2

# Create your views here.
def Taller2(request):
    Taller2s = taller2.objects.all().order_by('-date')
    return render(request, 'Taller2.html', {'Taller2s':Taller2s})