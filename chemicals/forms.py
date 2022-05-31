from django import forms
from master_data.models import Suppliers
from .models import Chemicals, Prices, Sds



################################## Chemicals Section
class ChemicalModelForm(forms.ModelForm):
    class Meta:
        model = Chemicals
        fields = ('description', 'cov', 'tanning', 'finishing', 'notes', 'flamability_status')
        
        widget = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'cov': forms.DecimalField(),
            'tanning': forms.BooleanField(),
            'finishing': forms.BooleanField(),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'flamability_status': forms.ChoiceField()
        }