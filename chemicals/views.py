from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from itertools import chain
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from .models import Chemicals, Prices, PricesManager, Sds
from django.db.models import Max, Prefetch, Subquery, OuterRef, FilteredRelation,Q

# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=2)
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)    
    return render(request, 'chemicals/suppliers_list.html', {'filter': suppliers_filter})


def price_list(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    chemicals_list = Chemicals.objects.filter(id_supplier=pk)

    qs=Prices.objects.all()
    
    prova=qs.values('id_chemical').annotate(latest_price=Max('price_date'))
    qs=qs.filter(Q(price_date__in=prova.values('latest_price').order_by('-price_date'))|Q(id_chemical__isnull=True)).filter(id_chemical__id_supplier=pk)
    for qs in qs:
        print("QS chem: " + str(qs.id_chemical))
        print("QS prezzo: " + str(qs.price))
        print("QS data: " + str(qs.price_date))
        print("QS cov: " + str(qs.id_chemical.cov))
    
    
    qs1=Sds.objects.all()
    prova_sds=qs1.values('id_chemical').annotate(latest_sds=Max('rev_date'))
    sds=qs1.filter(rev_date__in=prova_sds.values('latest_sds')).order_by('-rev_date').filter(id_chemical__id_supplier=pk)
    
    for sds in sds:
        print("sds chem: " + str(sds.id_chemical))
        print("sds sds: " + str(sds.sds))
        print("sds data: " + str(sds.rev_date))
        
    
        
    print("Chem: " + str(chemicals_list))
    #v=Chemicals.objects.filter(id_supplier=pk).annotate(latest_price=FilteredRelation('prices', condition=Q(Max('price_date')))).values('id_chemical', 'latest_price__price')
    #print("v: " + str(v))
    
    last_price=Prices.objects.max_of_prices()
    prezzi= Prices.objects.all().order_by('id_chemical', '-price_date').distinct('id_chemical')
    
    last_price_1=chemicals_list

    
    
    chem_price=chemicals_list
    
    #last_price=Prices.objects.values('id_chemical').annotate(Max('price_date')).distinct()
    
    #newest_price = Chemicals.objects.filter(id_supplier=pk).select_related('last_price')
    print("Chem_price: " + str(chem_price))
        
    #print("Newest: " + str(newest_price))
    print("Last: " + str(last_price))
    print("last_price_1: " + str(last_price_1))
    
    combined_list = list(chain(chemicals_list,last_price))    
    print("Combined: " + str(combined_list))
    context={'supplier': supplier, 'chemicals_list': chemicals_list, 'combined_list': combined_list, 'last_price': last_price, 'chem_price': chem_price, 'prezzi': prezzi, 'qs': qs}
    return render(request, "chemicals/price_list.html", context)


def update_product(request, pk):
    chemical = get_object_or_404(Chemicals, pk=pk)
    context={'chemical': chemical}
    return render(request, "chemicals/single_product.html", context)


