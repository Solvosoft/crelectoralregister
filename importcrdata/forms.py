from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from importcrdata.models import Distelec,PadronElectoral

class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput, required=False, label='')

class SearchLocationForm(forms.Form):
    province = forms.ModelMultipleChoiceField(widget=forms.Select, queryset = Distelec.objects.all().distinct('provincia'))

class SearchCantonForm(forms.Form):

    canton = forms.MultipleChoiceField(widget=forms.Select, choices =  [(x.codelec,x.canton) for x in Distelec.objects.filter(codelec__startswith='1').distinct('canton')])
    #
    # def __init__(self, foo_choices, *args, **kwargs):
    #
    #     super(SearchCantonForm, self).__init__(*args, **kwargs)
    #     print(kwargs)
    #     self.fields['canton'].choices = foo_choices


class CreatePerson(forms.ModelForm):

    class Meta:
        model = PadronElectoral
        fields = ('cedula','codelec','sexo','fechacaduc','junta','nombre','apellido1','apellido2')