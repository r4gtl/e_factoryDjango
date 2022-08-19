from django.shortcuts import render
from chemicals.models import ChemicalOrder
from chemicals.forms import OrderConformityForm

# Create your views here.

def homepage(request):
    orders = ChemicalOrder.objects.filter(conformity=False, n_conformity=False).order_by('-order_date')    
    form =OrderConformityForm()        
    context = {
        'orders': orders, 
        'form' : form,
        }
    return render(request, 'core/homepage.html', context)


