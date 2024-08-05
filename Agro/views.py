from django.shortcuts import render
from django.http import HttpResponse

from .models import Agro
# Create your views here.

def home(request):
    search_term = request.GET.get('searchProduct', '')
    category_filter = request.GET.get('category', 'Todos')

    if category_filter == 'Todos':
        agros = Agro.objects.filter(title__icontains=search_term)
    else:
        agros = Agro.objects.filter(title__icontains=search_term, category=category_filter)

    categories = Agro.objects.values_list('category', flat=True).distinct()
    categories = ['Todos'] + list(categories)  # Add "Todos" to the list of categories

    context = {
        'searchTerm': search_term,
        'agros': agros,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'home.html', context)
def about(request):
    #return HttpResponse('<h1>Welcome to About page</h1>')
    return render(request, 'about.html')