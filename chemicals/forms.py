from django import forms
from master_data.models import Suppliers
from .models import Chemicals, Prices, Sds



################################## Chemicals Section
class ChemicalModelForm(forms.ModelForm):
    class Meta:
        model = Chemicals
        fields = ('id_supplier', 'description', 'cov', 'tanning', 'finishing', 'notes', 'flamability_status')
        
        widget = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'cov': forms.DecimalField(),
            'tanning': forms.BooleanField(),
            'finishing': forms.BooleanField(),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'flamability_status': forms.ChoiceField(),
            'id_supplier': forms.HiddenInput()
        }
        
class SdsModelForm(forms.ModelForm):
    class Meta:
        model = Sds
        fields = ('id_chemical', 'sds', 'rev_date', 'conformityReach', 'reg_id')

        widget = {
            'id_chemical': forms.HiddenInput(),
            'sds': forms.FileField(),
            'rev_date': forms.DateField(),
            'conformityReach': forms.BooleanField(),            
            'reg_id': forms.ChoiceField(),            
        }