from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Suppliers
from .filters import SupplierFilter


def searchSupplier(request):
    suppliers_list = Suppliers.objects.all()
    suppliers_filter = SupplierFilter(request.GET, queryset=suppliers_list)
    
    return render(request, 'master_data/suppliers_list.html', {'filter': suppliers_filter})

class CreateSupplier(CreateView):
    model = Suppliers
    fields = "__all__"
    template_name = "master_data/create_supplier.html"
    success_url = "/"
    