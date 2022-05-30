from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from itertools import chain
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from .models import Chemicals, Prices, PricesManager, Sds
from django.db.models import Max, Prefetch, Subquery, OuterRef, FilteredRelation,Q, F

# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=2)
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)    
    return render(request, 'chemicals/suppliers_list.html', {'filter': suppliers_filter})


def price_list(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    chemicals_list = Chemicals.objects.filter(id_supplier=pk)
    chem_price=chemicals_list
    qs=Prices.objects.all()
    
    prova=qs.values('id_chemical').annotate(latest_price=Max('price_date'))
    print("Prima parte: " + str(prova))
    #qs=qs.filter(Q(price_date__in=prova.values('latest_price').order_by('-price_date'))|Q(price_date__isnull=True)).filter(id_chemical__id_supplier=pk)
    qs=qs.filter(price_date__in=prova.values('latest_price').order_by('-price_date')).filter(id_chemical__id_supplier=pk)
    #qs=qs.filter(price_date__in=prova.values('latest_price').order_by('-price_date'))
    '''
    for qs in qs:
        print("QS chem: " + str(qs.id_chemical))
        print("QS prezzo: " + str(qs.price))
        print("QS data: " + str(qs.price_date))
        print("QS cov: " + str(qs.id_chemical.cov))
    '''
    provaqs=Chemicals.objects.filter(id_supplier=pk).select_related('prezzo')
    #print('provaqs: ' + str(provaqs))
    
    
    #chem_price=chemicals_list
    #chem_price_1 = Chemicals.objects.filter(id_supplier=pk).prefetch_related('id_chemical__qs').all()

    
    chem_price_1 = Chemicals.objects.filter(id_supplier=pk).prefetch_related('id_chemical__qs', 'id_chemical__qs.price')
    #ModelA.objects.prefetch_related('modelb_set').all()
    #for chem in chem_price_1:
     #   print("chem_price_1 price: " + str(chem.price))   

    print("chem_price_1: " + str(chem_price_1))
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
    
    last_price=Prices.objects.max_of_prices(1)

    print("last: " +str(last_price))
    #print("Last chem: " + str(last_chem))
    for price in last_price:
        print("last: " +str(price.id_chemical))

    
    last_price_1=chemicals_list
    #print("Newest: " + str(newest_price))
    print("Last: " + str(last_price))
    print("last_price_1: " + str(last_price_1))
    
    
    context={'supplier': supplier, 'chemicals_list': chemicals_list, 'last_price': last_price, 'qs': qs, 'chem_price': chem_price}
    return render(request, "chemicals/price_list.html", context)


def update_product(request, pk):
    chemical = get_object_or_404(Chemicals, pk=pk)
    context={'chemical': chemical}
    return render(request, "chemicals/single_product.html", context)


