from django import forms
from importcrdata.models import Distelec, PadronElectoral


class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput, required=False, label='')


class PadronForm(forms.ModelForm):
    """
    In this class is the form for add a new person to the Padron Electoral Table.
    It needs cedula, codele, sexo, fechacaduc, junta and nombre_completo.
    """
    cedula = forms.CharField(max_length=9, widget=forms.TextInput(
        attrs={
            'class': 'form-control m-2',
            'placeholder': 'Cedula...'

        }
    ))

    codele = forms.CharField(max_length=6, widget=forms.TextInput(
        attrs={
            'class': 'form-control m-2',
            'placeholder': 'Codigo electoral...'

        }
    ))

    sexo = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control m-2',
            'min': "1",
            'max': "2",
        }
    ))

    fechacaduc = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={
            'class': 'form-control m-2',
            'placeholder': 'Fecha de caducidad...'
        }
    ))

    junta = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={
            'class': 'form-control m-2',
            'placeholder': 'Junta'
        }
    ))

    nombre_completo = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control m-2',
            'placeholder': 'Nombre completo....'
        }
    ))

    class Meta:
        model = PadronElectoral
        fields = ['cedula', 'codele', 'sexo', 'fechacaduc', 'junta', 'nombre_completo']
