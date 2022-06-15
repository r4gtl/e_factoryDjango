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
            'n_order': forms.IntegerField(),
            'id_supplier': forms.ChoiceField(),
            'order_date': forms.DateField(),
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
        