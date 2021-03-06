from django.db.models.fields import BooleanField
import django_filters
from django import forms
from django.db import models
from django_filters import DateFilter
from django_filters.filters import BooleanFilter
from .models import ChemicalOrder, Substances
from crispy_forms.bootstrap import InlineRadios



class OrderFilter(django_filters.FilterSet):
        n_ordine=django_filters.CharFilter(field_name='n_order', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label="")
        supplier=django_filters.CharFilter(field_name='id_supplier__company_name', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 7%'}), label="")
        
        class Meta:
            model = ChemicalOrder
            fields = ['n_ordine', 'supplier']
                
            filter_overrides = {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                        'widget' : forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
                        
                    },
                },               
            }
            
            
        
        #exclude = ['id_dett_ord', 'idcliente', 'idcollegamento']
        
class SubstancesFilter(django_filters.FilterSet):
        descrizione=django_filters.CharFilter(field_name='description', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label="")
        ec_number=django_filters.CharFilter(field_name='ec_number', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label="")
        cas_number=django_filters.CharFilter(field_name='cas_number', lookup_expr='icontains', widget=forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'}), label="")
                
        class Meta:
            model = Substances
            fields = ['description', 'ec_number', 'cas_number']
                
            filter_overrides = {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                        'widget' : forms.TextInput(attrs={'style': 'width: 90%; margin-left: 5%'})
                        
                    },
                },               
            }
