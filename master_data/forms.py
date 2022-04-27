from django import forms
from .models import Suppliers, SuppliersContacts

class SupplierModelForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ('company_name', 'vat_number','cf_number', 
                'address', 'cap', 'city', 'prov', 'country_state', 'gg_valuta', 
                'sds_path', 'category', 'vat_perc'
                )
        
        widget = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cf_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'cap': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'prov': forms.TextInput(attrs={'class': 'form-control'}),
            'country_state': forms.TextInput(attrs={'class': 'form-control'}),
            'gg_valuta': forms.TextInput(attrs={'class': 'form-control'}),
            'sds_path': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'vat_perc': forms.TextInput(attrs={'class': 'form-control'}),
            
            
        }

class SupplierContactsModelForm(forms.ModelForm):
    class Meta:
        model = SuppliersContacts
        fields = ('contact_name', 'email','phone_number', 
                'mobile', 'notes', 'id_supplier'
                )
        
        widget = {
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'id_supplier': forms.HiddenInput()

        }