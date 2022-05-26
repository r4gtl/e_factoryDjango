from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from itertools import chain
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from .models import Chemicals, Prices
from django.db.models import Max

# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=3)
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)    
    return render(request, 'chemicals/suppliers_list.html', {'filter': suppliers_filter})


def price_list(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    chemicals_list = Chemicals.objects.filter(id_supplier=pk)
    print("Chem: " + str(chemicals_list))
    #last_price=Prices.objects.values('id_chemical').order_by('-price_date').distinct()
    
    last_price=Prices.objects.values('id_chemical').annotate(Max('price_date')).distinct()
    newest_price = Chemicals.objects.filter(id_supplier=pk).select_related('last_price')
    
    print("Newest: " + str(newest_price))
    print("Last: " + str(last_price))
    
    combined_list = list(chain(chemicals_list,newest_price))    
    print("Combined: " + str(combined_list))
    context={'supplier': supplier, 'chemicals_list': chemicals_list, 'combined_list': combined_list, 'last_price': last_price}
    return render(request, "chemicals/price_list.html", context)


def update_product(request, pk):
    chemical = get_object_or_404(Chemicals, pk=pk)
    context={'chemical': chemical}
    return render(request, "chemicals/single_product.html", context)


