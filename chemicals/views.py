import errno
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from itertools import chain
from django_filters.views import FilterView
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from .forms import (
    ChemicalModelForm, SdsModelForm, 
    SubstanceSdsModelForm,PrecautionaryStatementSdsModelForm, 
    HazardStatementSdsModelForm, DangerSymbolsSdsModelForm, 
    ChemicalOrderModelForm, ChemicalOrderDetailModelForm,
    )

from .models import (
    Chemicals, Prices, PricesManager, 
    Sds, ChemicalHazardStatements, Substances, 
    ChemicalsSubstances, ChemicalsPrecautionaryStatement, 
    ChemicalDangerSymbols, DangerSymbols,
    ChemicalOrder, ChemicalOrderDetail,
    )

from .filters import OrderFilter
#from django.db.models import Max, Prefetch, Subquery, OuterRef, FilteredRelation,Q, F
from master_data.mixins import StaffMixin

# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=2)
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)    
    return render(request, 'chemicals/suppliers_list.html', {'filter': suppliers_filter})


def price_list(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    chemicals_list = Chemicals.objects.filter(id_supplier=pk)    
    
    context={'supplier': supplier, 'chemicals_list': chemicals_list}
    return render(request, "chemicals/price_list.html", context)


def update_product(request, pk):
    chemical = get_object_or_404(Chemicals, pk=pk)
    form = ChemicalModelForm(request.POST or None, instance=chemical)
    prices = Prices.objects.filter(id_chemical=pk).order_by('-price_date')
    sds=Sds.objects.filter(id_chemical=pk)
    if request.method == 'POST':
                
                if form.is_valid():
                        chemical_saved = form.save(commit=False)
                        chemical_saved.save()
                        #Non funziona                        
                        return HttpResponseRedirect(reverse('chemicals:search-supplier'))
    else:                
            form = ChemicalModelForm(instance=chemical)

    context={'chemical': chemical, 'prices': prices, 'sds': sds, 'form': form}
    return render(request, "chemicals/single_product.html", context)

class CreateProduct(StaffMixin, CreateView):
    model = Chemicals
    form_class = ChemicalModelForm    
    template_name = "chemicals/single_product.html"
    #success_url = "chemicals/suppliers_list.html"
    
    def form_valid(self, form):        
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)

def new_product(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    
    form = ChemicalModelForm(instance=supplier)
    if request.method == "POST":
        form = ChemicalModelForm(request.POST)        
        if form.is_valid():            
            form.save(commit=False)            
            form.instance.id_supplier = supplier            
            form.save()

            url_chemical = reverse("chemicals:price-list", kwargs={"pk": pk})            

            return HttpResponseRedirect(url_chemical)
        else:                       
            return HttpResponseBadRequest()
    
    context={'supplier': supplier, 'form': form}
    return render(request, "chemicals/single_product.html", context)


def delete_product(request, pk):
    obj = get_object_or_404(Chemicals, pk=pk)
    if request.method == "POST":
        parent_obj_url = obj.id_supplier.get_absolute_url()
        obj.delete()
        #return HttpResponseRedirect(parent_obj_url)
        url_chemical = reverse("chemicals:price-list", kwargs={"pk": obj.id_supplier.pk })
        print(url_chemical)

        return HttpResponseRedirect(url_chemical)
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)


'''Sezione Schede di sicurezza'''

def new_sds(request,pk):
    '''ATTENZIONE!!! LE VOCI DEVONO ESSERE COLLEGATE ALL'ID SCHEDA!!!'''
    chemical = get_object_or_404(Chemicals, pk=pk)
    
    #chemicals=Chemicals.objects.all()
    print("Chemical: " + str(chemical.pk))    
    substances = ChemicalsSubstances.objects.filter(id_chemical=pk)
    precautionary_statements=ChemicalsPrecautionaryStatement.objects.filter(id_chemical=pk)
    hazard_statements=ChemicalHazardStatements.objects.filter(id_chemical=pk)
    danger_symbols=ChemicalDangerSymbols.objects.filter(id_chemical=pk)


    form = SdsModelForm(instance=chemical)
    if request.method == "POST":
        form = SdsModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_chemical = chemical
            form.save()
            
            url_chemical = reverse("chemicals:single-product", kwargs={"pk": pk})
            print(url_chemical)

            return HttpResponseRedirect(url_chemical)
        else:
            print("Eco")
            print(form.errors)
            return HttpResponseBadRequest()
    
    context={
        'chemical': chemical, 
        'form': form,
        'substances': substances,
        'precautionary_statements': precautionary_statements,
        'hazard_statements': hazard_statements,
        'danger_symbols': danger_symbols,
        #'chemicals': chemicals
        }
    return render(request, "chemicals/safety_data_sheet.html", context)


class UpdateSds(UpdateView):
    model = Sds
    form_class = SdsModelForm
    template_name = "chemicals/safety_data_sheet.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['substances'] = ChemicalsSubstances.objects.filter(id_sds=self.kwargs['pk'])
        context['danger_symbols'] = ChemicalDangerSymbols.objects.filter(id_sds=self.kwargs['pk'])
        context['precautionary_statements'] = ChemicalsPrecautionaryStatement.objects.filter(id_sds=self.kwargs['pk'])
        context['hazard_statements'] = ChemicalHazardStatements.objects.filter(id_sds=self.kwargs['pk'])        
        return context
    
    def form_valid(self, form):        
        self.success_url = self.request.POST.get('previous_page')
        
        return super().form_valid(form)


def update_sds(request, id, pk):
        print("ID: " + str(id))
        print("PK: " + str(pk))
        sds = get_object_or_404(Sds, pk=pk)
        print("Sds: " + str(sds.pk))
        chemical=get_object_or_404(Chemicals, pk=id)
        
        
        substances = ChemicalsSubstances.objects.filter(id_sds=sds.pk)
        precautionary_statements=ChemicalsPrecautionaryStatement.objects.filter(id_sds=pk)
        hazard_statements=ChemicalHazardStatements.objects.filter(id_sds=pk)
        danger_symbols=ChemicalDangerSymbols.objects.filter(id_sds=pk)
        
        form = SdsModelForm(request.POST or None, instance = sds)
        
        if request.method == 'POST':
                
                if form.is_valid():
                        sds_saved = form.save(commit=False)
                        sds_saved.save()
                        #Non funziona
                        
                        return HttpResponseRedirect(reverse('chemicals/safety_data_sheet.html', kwargs={"id": id, "pk": pk}))
        else:
                
                form = SdsModelForm(instance=sds)
        context = {
            'chemical': chemical, 
            'form': form,
            'substances': substances,
            'precautionary_statements': precautionary_statements,
            'hazard_statements': hazard_statements,
            'danger_symbols': danger_symbols,
            }        
        return render(request, "chemicals/safety_data_sheet.html", context)




def new_substance_sds(request,pk):
    
    sds = get_object_or_404(Sds, pk=pk)
    #chemical=Chemicals.objects.filter(pk=sds.id_chemical.pk)  
    chemical=Chemicals.objects.get(pk=sds.id_chemical.pk)  
    print("Chemical: " + str(chemical))      
    form = SubstanceSdsModelForm(instance=sds)
    if request.method == "POST":
        form = SubstanceSdsModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_chemical = chemical.pk
            form.instance.id_sds = sds
            form.save()
            
            url_sds = reverse("chemicals:new-substance-sds", kwargs={"id": chemical.id_chemical, "pk": pk})

            return HttpResponseRedirect(url_sds)
        else:
            print("Eco")
            print(form.errors)
            return HttpResponseBadRequest()
    
    context={
        'chemical': chemical, 
        'form': form,
        'sds': sds        
        }
    return render(request, "chemicals/substances_in_sds.html", context)


def new_ps_sds(request,pk):
    
    sds = get_object_or_404(Sds, pk=pk)
    chemical=Chemicals.objects.filter(pk=sds.id_chemical.pk)           
    form = PrecautionaryStatementSdsModelForm(instance=sds)
    if request.method == "POST":
        form = PrecautionaryStatementSdsModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_chemical = chemical.pk
            form.instance.id_sds = sds
            form.save()
            
            url_ps = reverse("chemicals:new-ps-sds", kwargs={"id": chemical.id_chemical, "pk": pk})

            return HttpResponseRedirect(url_ps)
        else:
            print("Eco")
            print(form.errors)
            return HttpResponseBadRequest()
    
    context={
        'chemical': chemical, 
        'form': form,
        'sds': sds        
        }
    return render(request, "chemicals/ps_in_sds.html", context)

def new_hs_sds(request,pk):
    
    sds = get_object_or_404(Sds, pk=pk)
    chemical=Chemicals.objects.filter(pk=sds.id_chemical.pk)           
    form = HazardStatementSdsModelForm(instance=sds)
    if request.method == "POST":
        form = HazardStatementSdsModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_chemical = chemical.pk
            form.instance.id_sds = sds
            form.save()
            
            url_hs = reverse("chemicals:new-hs-sds", kwargs={"id": chemical.id_chemical, "pk": pk})

            return HttpResponseRedirect(url_hs)
        else:
            print("Eco")
            messages.error(request, "prova")
            print(form.errors)
            #return redirect("chemicals:new-hs-sds")
            #return HttpResponseBadRequest()
    
    context={
        'chemical': chemical, 
        'form': form,
        'sds': sds        
        }
    return render(request, "chemicals/hs_in_sds.html", context)


def new_ds_sds(request, id, pk):
    
    sds = get_object_or_404(Sds, pk=pk)
    print("Nuova pk:" + str(pk))
    symbols = DangerSymbols.objects.all()
    chemical=Chemicals.objects.get(pk=sds.id_chemical.pk) 
    print("Chemical:" + str(chemical.id_chemical))          
    form = DangerSymbolsSdsModelForm(instance=sds)
    if request.method == "POST":
        form = DangerSymbolsSdsModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_chemical = chemical
            form.instance.id_sds = sds
            form.save()
            
            url_ds = reverse("chemicals:update-sds", kwargs={"id": id, "pk": pk})

            return HttpResponseRedirect(url_ds)
        else:
            print("Eco")
            print(form.errors)
            messages.error(request, "Hai già inserito questo simbolo in questa scheda")
            #return HttpResponseBadRequest()
    
    context={
        'chemical': chemical, 
        'form': form,
        'sds': sds,
        'symbols': symbols
        }
    return render(request, "chemicals/ds_in_sds.html", context)


'''Fine Sezione Schede di sicurezza'''



'''Sezione Ordini'''
'''In questa sezione ci sono tutte le views per gestire gli ordini di prodotti chimici'''

class OrderList(FilterView):
    '''Ottenere un elenco degli ordini con filtraggio'''
    queryset = ChemicalOrder.objects.all().order_by('-order_date')
    template_name = "chemicals/orders_list.html"
    filterset_class = OrderFilter
    context_object_name = "order_list"


class CreateOrder(CreateView):
    model = ChemicalOrder
    form_class = ChemicalOrderModelForm    
    template_name = "chemicals/order.html"
    #success_url = "chemicals/suppliers_list.html"
    context_object_name = 'order'
    
    def form_valid(self, form):        
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        print(context)
        # Add in a QuerySet of all the books
        if self.request=='GET':
            context['order_detail'] = ChemicalOrderDetail.objects.filter(id_order=self.kwargs['id_order'])
            print(context['order_detail'])
            context['order_instance'] = ChemicalOrder.objects.get(id_order=self.kwargs['id_order'])               
        return context
    
    

'''
class CreateDetail(CreateView):
    model = ChemicalOrderDetail
    
    form_class = ChemicalOrderDetailModelForm
    template_name = "chemicals/order_detail.html"
    #success_url="chemicals/order.html"


    def get_object(self):
        #Mi prendo l'istanza dell'Ordine dalla pagina che sto lasciando
        pk = self.kwargs.get('pk')
        order_instance = get_object_or_404(ChemicalOrder, pk=pk)        
        return order_instance

    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Mi prendo l'elenco dei prodotti acquistati dal fornitore dell'ordine        
        context['chemical_list'] = Chemicals.objects.filter(id_supplier=self.get_object().pk)        
        print("Context: " + str(context['chemical_list']))        
        return context

    def form_valid(self, form): 
               
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)
'''

def create_detail(request,pk):
    order=ChemicalOrder.objects.get(id_order=pk)
    print(order)
    print("Ordine: " + str(order.pk))
    
    supplier=get_object_or_404(Suppliers, pk=order.id_supplier.pk)  
    form= ChemicalOrderDetailModelForm(supplier.pk, order)
    if request.method == 'POST':
        print("Request: POST")
        form = ChemicalOrderDetailModelForm(supplier.pk, order, request.POST)
        
        if form.is_valid():
            print("Valido")

            print(form.cleaned_data)
            form.save(commit=False)
            form.instance.id_order = order
            form.save()
            url_hs = reverse("chemicals:update-order", kwargs={"pk": order.id_order})
            return HttpResponseRedirect(url_hs)
        
    else:
        form = ChemicalOrderDetailModelForm(supplier.pk, order)
    context={
        'order': order, 
        'form': form,
        'supplier': supplier        
        }
    return render(request, 'chemicals/order_detail.html', context)

def load_last_orders_view(request, id_chemical):
    qs = ChemicalOrderDetail.objects.filter(id_chemical=id_chemical)    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data=[]
        for obj in qs:
            item = {
                'id_detail': obj.id_detail,
                'id_order': obj.id_order.n_order,
                'order_date':obj.id_order.order_date,
                'id_chemical': obj.id_chemical.description,
                'um': obj.um,
                'quantity': obj.quantity,
                'id_packaging_type': obj.id_packaging_type.description
            }
            data.append(item)        
        return JsonResponse({'data': data})

def load_chemicals_to_search(request, id_supplier):
    qs = Chemicals.objects.filter(id_supplier=id_supplier)      
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data=[]
        for obj in qs:
            print("Obj:" + str(obj.id_chemical))
            instance = Chemicals.objects.get(id_chemical=obj.id_chemical)
            print("Instance:" + str(instance))
            price=instance.get_price()
            print("Prezzo: " + str(price))
            item = {
                'id_chemical': obj.description,
                'id_supplier': instance.get_price(),
                'description': str(obj.cov),                
            }
            data.append(item)
        print("COV: " + str(data))        
        return JsonResponse({'data': data})



class UpdateOrder(UpdateView):
    model = ChemicalOrder
    form_class = ChemicalOrderModelForm
    template_name = "chemicals/order.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books   
        # 
        context['order_detail'] = ChemicalOrderDetail.objects.filter(id_order=self.kwargs['pk'])
        context['order_instance'] = ChemicalOrder.objects.get(id_order=self.kwargs['pk'])            
        print(context)
        return context
    
    def form_valid(self, form):        
        self.success_url = self.request.POST.get('previous_page')
        
        return super().form_valid(form)


'''Fine Sezione Ordini'''

