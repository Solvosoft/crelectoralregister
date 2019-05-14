from django import forms



class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput, required=False, label='')

