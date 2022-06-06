from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from itertools import chain
from master_data.models import Suppliers
from master_data.forms import SupplierModelForm
from master_data.filters import SupplierFilter
from .forms import ChemicalModelForm
from .models import Chemicals, Prices, PricesManager, Sds
from django.db.models import Max, Prefetch, Subquery, OuterRef, FilteredRelation,Q, F
from master_data.mixins import StaffMixin

# Create your views here.

def home(request):
    suppliers_list = Suppliers.objects.filter(category=3)
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
            print(url_chemical)

            return HttpResponseRedirect(url_chemical)
        else:
            
            return HttpResponseBadRequest()
    
    context={'supplier': supplier, 'form': form}
    return render(request, "chemicals/single_product.html", context)


# class CancellaProdotto(DeleteView):
#     template_name ='confirm_delete.html'
#     model = Chemicals
#     success_url = "chemicals:price-list"

def delete_product(request, pk):
    obj = get_object_or_404(Chemicals, pk=pk)
    if request.method == "POST":
        parent_obj_url = obj.id_supplier.get_absolute_url()
        obj.delete()
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)


def addSds():
    pass




