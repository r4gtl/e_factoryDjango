from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from .models import Suppliers, SuppliersContacts
from .filters import SupplierFilter
from .mixins import StaffMixin
from .forms import SupplierModelForm, SupplierContactsModelForm


def searchSupplier(request):
    suppliers_list = Suppliers.objects.all()
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)
    
    return render(request, 'master_data/suppliers_list.html', {'filter': suppliers_filter})

class CreateSupplier(StaffMixin, CreateView):
    model = Suppliers
    form_class = SupplierModelForm
    #fields = "__all__"
    template_name = "master_data/create_supplier.html"
    success_url = "master_data:search-supplier"
    
class UpdateSupplier(UpdateView):
    model = Suppliers
    form_class = SupplierModelForm
    # fields = "__all__"
    template_name = "master_data/update_supplier.html"
    success_url = "master_data/suppliers_list.html"


def create_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    contacts = SuppliersContacts.objects.filter(id_supplier=pk)
    
    if request.method == "POST":
        form = SupplierModelForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)           
            supplier.save()
            
            return HttpResponseRedirect("master_data:search-supplier")
            #return HttpResponseRedirect(supplier.get_absolute_url())
    else:
        form = SupplierModelForm()
    context = {"form": form, "supplier": supplier}
    return render(request, "forum/create_supplier.html", context)
    
    
def update_supplier(request, pk):
        supplier = get_object_or_404(Suppliers, pk=pk)
        contacts = SuppliersContacts.objects.filter(id_supplier=pk)
        
        form = SupplierModelForm(request.POST or None, instance = supplier)
        
        if request.method == 'POST':
                
                if form.is_valid():
                        supplier_saved = form.save(commit=False)
                        supplier_saved.save()
                        #Non funziona
                        
                        return HttpResponseRedirect(reverse('master_data:search-supplier'))
        else:
                
                form = SupplierModelForm(instance=supplier)
        context = {"supplier": supplier, "contacts": contacts, 'form':form}        
        return render(request, "master_data/create_supplier.html", context)


def new_contact(request,pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    form = SupplierContactsModelForm(instance=supplier)
    if request.method == "POST":
        form = SupplierContactsModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id_supplier = supplier
            form.save()

            url_supplier = reverse("master_data:update-supplier", kwargs={"pk": pk})
            print(url_supplier)

            return HttpResponseRedirect(url_supplier)
        else:
            
            return HttpResponseBadRequest()
    
    context={'supplier': supplier, 'form': form}
    return render(request, "master_data/create_supplier_contact.html", context)


class UpdateContact(UpdateView):
    model = SuppliersContacts
    form_class = SupplierContactsModelForm
    template_name = "master_data/create_supplier_contact.html"
    
    def form_valid(self, form):        
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)

    