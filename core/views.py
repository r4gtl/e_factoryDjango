from django.shortcuts import render
from chemicals.models import ChemicalOrder

# Create your views here.

def homepage(request):
    orders = ChemicalOrder.objects.filter(conformity=False, n_conformity=False).order_by('-order_date')
    context = {"orders": orders}
    return render(request, 'core/homepage.html', context)


