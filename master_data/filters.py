import django_filters
from .models import Suppliers, VatCodes

# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', ]
        
class SupplierFilter(django_filters.FilterSet):
    company_name=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Suppliers
        fields = ['company_name', 'vat_number', 'cf_number'] 
        