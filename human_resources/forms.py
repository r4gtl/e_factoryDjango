from cProfile import label
from django import forms
from .models import HumanResource


class HumanResourceModelForm(forms.ModelForm):
    class Meta:
        model = HumanResource
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

        widget = {
            'idpersona': forms.HiddenInput(),
            'cognomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'nomedipendente': forms.TextInput(attrs={'class': 'form-control'}),
            'immagine': forms.ImageField(),
            'gender': forms.ChoiceField(),
            'dataassunzione': forms.DateInput(),
            'datadimissioni': forms.DateInput(),
            'idmansione': forms.ChoiceField(),
            'idreparto': forms.ChoiceField(),
            'qualifica': forms.TextInput(attrs={'class': 'form-control'}),
            'commenti': forms.Textarea(attrs={'class': 'form-control'}),
            
        },
        labels = {
            'cognomedipendente': 'Cognome',
            'nomedipendente': 'Nome',
            'immagine': 'Foto',
            'gender': 'Genere',
            'dataassunzione': 'Data Assunzione',
            'datadimissioni': 'Data Dimissioni',
            'idmansione': 'Mansione',
            'idreparto': 'Reparto',
            'qualifica': 'Qualifica',
            'commenti': 'Commenti',

        }
        