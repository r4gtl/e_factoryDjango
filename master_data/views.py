from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .models import Suppliers, SuppliersContacts
from .filters import SupplierFilter
from .mixins import StaffMixin
from .forms import SupplierModelForm


def searchSupplier(request):
    suppliers_list = Suppliers.objects.all()
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)
    
    return render(request, 'master_data/suppliers_list.html', {'filter': suppliers_filter})

class CreateSupplier(StaffMixin, CreateView):
    model = Suppliers
    form_class = SupplierModelForm
    #fields = "__all__"
    template_name = "master_data/create_supplier.html"
    success_url = "/"
    
class UpdateSupplier(UpdateView):
    model = Suppliers
    form_class = SupplierModelForm
    # fields = "__all__"
    template_name = "master_data/update_supplier.html"


def create_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    contacts = SuppliersContacts.objects.filter(id_supplier=pk)
    
    if request.method == "POST":
        form = SupplierModelForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)           
            supplier.save()
            
            return HttpResponseRedirect(supplier.get_absolute_url())
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
                        return HttpResponseRedirect(supplier.get_absolute_url())
        else:
                
                form = SupplierModelForm(instance=supplier)
        context = {"supplier": supplier, "contacts": contacts, 'form':form}        
        return render(request, "master_data/create_supplier.html", context)


def new_contact(request,pk):
    pass
#def aggiungi_nomeincarico(request, pk):
 #   operatore = get_object_or_404(Dipendenti, pk=pk)
  #  form = NomiIncarichiModelForm(instance=operatore)
   # if request.method == "POST":
    #    form = NomiIncarichiModelForm(request.POST)
     #   if form.is_valid():
      #      form.save(commit=False)
       #     form.instance.operatore = operatore
        #    # form.instance.autore_post = request.user
         #   form.save()
            
          #  url_operatore = reverse("operatore_view", kwargs={"pk": pk})
            
            
    #        return HttpResponseRedirect(url_operatore)
    #    else:
     #       return HttpResponseBadRequest()
    #context={'operatore': operatore, 'form': form}
    #return render(request, 'human_resources/aggiungi_incarico.html', context)