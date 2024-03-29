from ctypes.wintypes import SIZEL
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models import Max, Prefetch,Count, Subquery,OuterRef
from itertools import chain
from django_filters.views import FilterView
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from django.db import models, connection

from .forms import (
    ChemicalModelForm, SdsModelForm,
    SubstanceSdsModelForm,PrecautionaryStatementSdsModelForm,
    HazardStatementSdsModelForm, DangerSymbolsSdsModelForm,
    ChemicalOrderModelForm, ChemicalOrderDetailModelForm,
    OrderConformityForm
    )

from .models import (
    Chemicals, Prices, 
    Sds, ChemicalHazardStatements, Substances,
    ChemicalsSubstances, ChemicalsPrecautionaryStatement,
    ChemicalDangerSymbols, DangerSymbols,
    ChemicalOrder, ChemicalOrderDetail,
    ChemicalPurchase, ChemicalPurchaseDetail,
    )

from .filters import OrderFilter, ChemicalFilter, PurchaseFilter
#from django.db.models import Max, Prefetch, Subquery, OuterRef, FilteredRelation,Q, F
from master_data.mixins import StaffMixin
from django.core.paginator import Paginator
from django.core import serializers
import json





# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=2)
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)
    return render(request, 'chemicals/suppliers_list.html', {'filter': suppliers_filter})


def price_list(request,pk):    
    latest_price= Prices.objects.get_max_of_price()
    latest_rev=Sds.objects.get_max_of_sds()    
    supplier = get_object_or_404(Suppliers, pk=pk)        
    chem_list=Chemicals.objects.filter(id_supplier=pk).order_by('description').prefetch_related(
            Prefetch('prezzo',
                    queryset=latest_price,
                    to_attr='latest_price'
                    )            
        ).prefetch_related(
            Prefetch('sds',
                    queryset=latest_rev,
                    to_attr='latest_rev'
                    )            
        )  
    
    chem_filter = ChemicalFilter(request.GET, queryset=chem_list)
    
    # discussione = get_object_or_404(Discussione, pk=pk)
    # posts_discussione = Post.objects.filter(discussione=discussione)

    # paginator = Paginator(posts_discussione, 5)
    # page = request.GET.get("pagina")
    # posts = paginator.get_page(page)

    # form_risposta = PostModelForm()
    # context = {
    #     "discussione": discussione,
    #     "posts_discussione": posts,
    #     "form_risposta": form_risposta,
    # }
    
    # paginator = Paginator(chem_filter.qs, 30)    
    # page = request.GET.get("pagina")
    # chem_page=paginator.get_page(page)
    context={'supplier': supplier, 'chemicals_list': chem_list, 'filter': chem_filter}
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
        # chemical aggiunto per attivare il pulsante "annulla"
        context['chemical'] = get_object_or_404(Chemicals, id_chemical=self.object.id_chemical.id_chemical)
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
    substance_modal = Substances.objects.all()
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
        'sds': sds,
        'substance_modal': substance_modal
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


'''SEZIONE ACQUISTI'''
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
        # self.success_url = self.request.POST.get('previous_page')
        # return super().form_valid(form)
        pass
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the orders
        if self.request=='GET':
            context['order_detail'] = ChemicalOrderDetail.objects.filter(id_order=self.kwargs['id_order'])
            context['order_instance'] = ChemicalOrder.objects.get(id_order=self.kwargs['id_order'])
        return context


def create_detail(request,pk):
    order=ChemicalOrder.objects.get(id_order=pk)
    supplier=get_object_or_404(Suppliers, pk=order.id_supplier.pk)
    #form= ChemicalOrderDetailModelForm(supplier.pk, order)
    if request.method == 'POST':
        form = ChemicalOrderDetailModelForm(supplier.pk, order, request.POST)

        if form.is_valid():

            form.save(commit=False)
            form.instance.id_order = order
            form.save()
            if 'save' in request.POST:
                url_hs = reverse("chemicals:update-order", kwargs={"pk": order.id_order})
            else:
                url_hs = reverse("chemicals:add-detail", kwargs={"pk": order.id_order})
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
    '''
    Questa view serve per caricare gli ultimi ordini effettuati del prodotto scelto
    '''
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
    
def load_chemicals_to_search(request, id_supplier, num_chems):
    '''
    Carica i prodotti chimici del fornitore scelto
    '''
    visible = 3
    upper = num_chems
    lower = upper - visible 
    # Utilizzata la query nel manager dei prezzi   
    latest_price= Prices.objects.get_max_of_price()    
    qs=Chemicals.objects.filter(id_supplier=id_supplier).order_by('description').prefetch_related(
        Prefetch('prezzo',
                queryset=latest_price,                
                to_attr='latest_price'
                )
        
    )
    
    print("qs: " +str(qs))
    size = len(qs)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        data=[]
        for obj in qs:            
            if obj.latest_price:
                last_price=obj.latest_price[0].price,
            else:                
                last_price='Manca'
                    
            item = {
                'id_chemical': obj.description,                
                'last_price': last_price,   
                'cov': str(obj.cov),
                'pk_chem': obj.id_chemical,
            }            
            data.append(item) 
            
    
        return JsonResponse({'data': data[lower:upper], 'size': size})
    



def load_chemicals_to_search_filtered(request, id_supplier, search_text, num_chems):
    '''
    Carica i prodotti chimici del fornitore scelto filtrandoli man mano che si digita il nome
    '''
    
    visible = 3
    upper = num_chems
    lower = upper - visible
    
    # Utilizzata la query nel manager dei prezzi
    latest_price= Prices.objects.get_max_of_price()
    
    if search_text:
        
        qs=Chemicals.objects.filter(id_supplier=id_supplier).filter(description__icontains=search_text).order_by('description').prefetch_related(
            Prefetch('prezzo',
                    queryset=latest_price,
                    to_attr='latest_price'
                    )
            
        )   
    else:
        
        qs=Chemicals.objects.filter(id_supplier=id_supplier).order_by('description').prefetch_related(
            Prefetch('prezzo',
                    queryset=latest_price,
                    to_attr='latest_price'
                    )
            
        )
        
        #qs = Chemicals.objects.filter(id_supplier=id_supplier)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        size = len(qs)
        data=[]
        for obj in qs:
            if obj.latest_price:
                last_price=obj.latest_price[0].price,
            else:                
                last_price='Manca'     
            
            item = {
                'id_chemical': obj.description,
                
                'last_price': last_price,
                'description': str(obj.cov),
                'pk_chem': obj.id_chemical,
            }
            data.append(item)        
        return JsonResponse({'data': data[lower:upper], 'size': size})


def load_suppliers_to_search(request):
    '''
    Carica i fornitori da cercare
    '''
    qs = Suppliers.objects.all().order_by('company_name')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data=[]
        for obj in qs:
            item = {
                'id_supplier': obj.id_supplier,
                'company_name': obj.company_name,
            }
            data.append(item)
        return JsonResponse({'data': data})


def load_suppliers_to_search_filtered(request, search_text):
    '''
    Carica i fornitori filtrandoli man mano che si digita la ragione sociale
    '''
    qs = Suppliers.objects.filter(company_name__icontains=search_text).order_by('company_name')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data=[]
        for obj in qs:
            item = {
                'id_supplier': obj.id_supplier,
                'company_name': obj.company_name,
            }
            data.append(item)
        return JsonResponse({'data': data})





def load_substances_to_search_filtered(request, search_cas):
    '''
    Carica le sostanze filtrandoli man mano che si digita cas, nome o ec
    '''

    qs = Substances.objects.filter(cas_number__icontains=search_cas).order_by('description')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method=="GET":

            data=serializers.serialize('json',
                                    list(qs),
                                    fields=('id_substance', 'description', 'cas_number', 'ec_number')
                                    )            
    return JsonResponse(data, safe=False)


def load_substances_to_search(request):
    qs = Substances.objects.all().order_by('description')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        data=[]
        for obj in qs:
            item = {
                'id_substance': obj.id_substance,
                'description': obj.description,
                'cas_number': obj.cas_number,
                'ec_number': obj.ec_number,
            }
            data.append(item)
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
        return context

    def form_valid(self, form):
        self.success_url = self.request.POST.get('previous_page')

        return super().form_valid(form)
        

def update_conf_order(request, pk):
    order = get_object_or_404(ChemicalOrder, pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Arrivato!")
        new_conformity = request.POST.get('conformity')
        order.conformity = new_conformity
        order.save()
        return JsonResponse({
            'new_conformity':'new_conformity'
        })

    return redirect('core:homepage') # you should change that with the name of your view




'''Fine Sezione Ordini'''
'''Sezione Documenti di Acquisto'''
def purchaselist(request):
    purchase_list = ChemicalPurchase.objects.all()
    purchase_filter = PurchaseFilter(request.GET, queryset=purchase_list)
    return render(request, 'chemicals/purchase_list.html', {'filter': purchase_filter})

'''Fine Sezione Documenti di Acquisto'''

'''FINE SEZIONE ACQUISTI'''

