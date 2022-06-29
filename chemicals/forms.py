from django import forms
from master_data.models import Suppliers
from .models import (
    Chemicals, Prices, Sds, 
    ChemicalsSubstances, ChemicalsPrecautionaryStatement, 
    ChemicalHazardStatements, ChemicalDangerSymbols,
    ChemicalOrder, ChemicalOrderDetail
)



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
        labels = {
                'description': 'Nome Prodotto',
                'cov': 'Solvente',
                'tanning': 'Bagnato',
                'finishing': 'Rifinizione',
                'notes': 'Note',
                'flamability_status': 'Classe di Infiammabilità',
                
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
        labels = {
                'sds': 'Allega Scheda',
                'rev_date': 'Data Revisione',
                'conformityReach': 'Ok Reach',
                'reg_id': 'Regolamento Riferimento'
        }

class SubstanceSdsModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalsSubstances
        fields = ('id_chemical', 'id_sds', 'id_substance', 'concentration')

        widget = {
            'id_chemical': forms.HiddenInput(),
            'id_sds': forms.HiddenInput(),
            'id_substance': forms.CharField(),
            'concentration': forms.CharField(),            
                        
        }
        labels = {
                'id_substance': 'Nome Sostanza',
                'concentration': 'Concentrazione'                
        }
        
class PrecautionaryStatementSdsModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalsPrecautionaryStatement
        fields = ('id_chemical', 'id_sds', 'id_ps')

        widget = {
            'id_chemical': forms.HiddenInput(),
            'id_sds': forms.HiddenInput(),
            'id_ps': forms.CharField(),
            
                        
        }
        labels = {
                'id_ps': 'Consiglio di Prudenza'                
        }
        
        
        
class HazardStatementSdsModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalHazardStatements
        fields = ('id_chemical', 'id_sds', 'id_hs')

        widget = {
            'id_chemical': forms.HiddenInput(),
            'id_sds': forms.HiddenInput(),
            'id_hs': forms.CharField(),
            
                        
        }
        labels = {
                'id_hs': 'Frase di Rischio'                
        }


class DangerSymbolsSdsModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalDangerSymbols
        fields = ('id_chemical', 'id_sds', 'id_danger')

        widget = {
            'id_chemical': forms.HiddenInput(),
            'id_sds': forms.HiddenInput(),
            'id_danger': forms.CharField(),
        }
        labels = {
                'id_danger': 'Simbolo di Pericolo'                
        }

'''Sezione Ordini'''
class ChemicalOrderModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalOrder
        fields = (
            'id_order',
            'n_order',
            'id_supplier',
            'order_date',
            'delivery_date',
            'notes',
            'user_id',
            'conformity',
            'n_conformity',
            'n_conformity_reasons',
            'operator',
            'id_dich_int'
        )
        widget = {
            'id_order': forms.HiddenInput(),
            'n_order': forms.TextInput(),
            'id_supplier': forms.ChoiceField(),
            'order_date': forms.DateInput(),
            'delivery_date': forms.DateField(),
            'notes': forms.Textarea(),
            'user_id': forms.CharField(),
            'conformity': forms.BooleanField(),
            'n_conformity': forms.BooleanField(),
            'n_conformity_reasons': forms.Textarea(),
            'operator': forms.CharField(),
            'id_dich_int': forms.HiddenInput()
        }
        labels = {
            'n_order': 'Ordine N.',
            'id_supplier': 'Fornitore',
            'order_date': 'Data Ordine',
            'delivery_date': 'Data Consegna',
            'notes': 'Note',
            'user_id': 'Redatto Da',
            'conformity': 'Conforme',
            'n_conformity': 'Non Conforme',
            'n_conformity_reasons': 'Non Conformità',
            'operator': 'Operatore'
        }

class ChemicalOrderDetailModelFormOld(forms.ModelForm):

    class Meta:
        model = ChemicalOrderDetail
        fields = (
            'id_detail', 
            'id_order', 
            'id_chemical',
            'um',
            'quantity',
            'id_packaging_type'
            )
        

        widget = {
            'id_detail': forms.HiddenInput(),
            'id_order': forms.HiddenInput(),
            'id_chemical': forms.ChoiceField(),            
            'um': forms.CharField(),
            'quantity':forms.CharField(),
            'id_packaging_type':forms.CharField()

        }
        labels = {                            
            'id_chemical': 'Prodotto',
            'um': 'Unità di Misura',
            'quantity':'Quantità',
            'id_packaging_type':'Aspetto dei beni'               
        }

        

class ChemicalOrderDetailModelForm(forms.ModelForm):
    class Meta:
        model = ChemicalOrderDetail
        fields = (
            'id_detail', 
            'id_order', 
            'id_chemical',
            'um',
            'quantity',
            'id_packaging_type'
            )
        widget = {
            'id_detail': forms.HiddenInput(),
            'id_order': forms.HiddenInput(),
            #'id_chemical': forms.ChoiceField(),            
            'um': forms.CharField(),
            'quantity':forms.CharField(),
            'id_packaging_type':forms.CharField()

        }
        labels = {                            
            'id_chemical': 'Prodotto',
            'um': 'Unità di Misura',
            'quantity':'Quantità',
            'id_packaging_type':'Aspetto dei beni'               
        }
    '''
    Con questa parte inizializzo la choicefield popolandolo con i soli 
    prodotti chimici del fornitore dell'ordine (vedi anche la view create_detail)
    '''
    def __init__(self, id_supplier, order, *args, **kwargs):
        super(ChemicalOrderDetailModelForm, self).__init__(*args, **kwargs)
        self.fields['id_chemical'].queryset = Chemicals.objects.filter(id_supplier=id_supplier)
        self.fields['id_order'].initial=order