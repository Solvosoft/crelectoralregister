from django.core.mail.backends import console
from django.shortcuts import render
from data.models import Padron_electoral, Distelec
from django.db.models import Count
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.

#implementado listView
class listViewData(ListView):

    template_name = 'test.html'
    model = Padron_electoral
    paginate_by = 15  # if pagination is desired
    queryset = Padron_electoral.objects.all()
    #context_object_name = 'data'
    #form_class=SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class distelecListView(ListView):
    template_name = 'distelec.html'
    model = Distelec
    paginate_by = 15
    queryset = Distelec.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class searchDetailView(ListView):
    model = Padron_electoral
    template_name = 'filterData.html'
    paginate_by = 15
    #context_object_name = 'search'
    #queryset = Padron_electoral.objects.filter(cedula__icontains=str('207000998'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['search'] = self.search
        #print(context, 'context')
        return context

    def get_queryset(self):
        queryset = Padron_electoral.objects.all()
        #self.search = get_object_or_404(Padron_electoral, self.kwargs['search'])
        if self.request.GET.get('search'):
            queryset = queryset.filter(search = self.request.GET.get('search'))
        return queryset
        #return Padron_electoral.objects.filter(search=self.search)
        #return render(request, "test.html", context=context)

    def searchData(request, self):
        print(request.GET.get('search', ""))
        search = request.GET.get('search', "")
        console.log(search, 'buscado')
        if type(search) == int:
            data = Padron_electoral.objects.filter(codelec_icontains=str(search))
        elif type(search) == int:
            data = Padron_electoral.objects.filter(cedula__icontains=str(search))
        elif type(search) == str:
            data = Padron_electoral.objects.filter(nombre__icontains=str(search))
        return render(request, 'filterData.html', context={'object_list':data})


def getInfoDistelec(request):
    info = request.GET.get('codele')
    query = Distelec.objects.filter(codele=info)
    return render(request, 'distelec.html', context={"query": query})

#BUSQUEDA POR CEDULA
#1.Mostrar la info de la persona buscada
def searchDataP(request, search):
    print(request.GET.get('search', ""))
    search = request.GET.get('search', "")
    console.log(search, 'buscado')
    if type(search) == int:
        data = Padron_electoral.objects.filter(codelec_icontains=str(search))
    elif type(search) == int:
        data = Padron_electoral.objects.filter(cedula__icontains=str(search))
    elif type(search) == str:
        data = Padron_electoral.objects.filter(nombre__icontains=str(search))
    return render(request, 'filterData.html', context={'object_list':data})

""""
def getSearch(request):
    form = forms.SearchForm()
    if request.method == "GET":
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['search'] != '':
                info = searchDataP(form.cleaned_data['search'])
        return render(request, 'filter.html', {'info': info, 'searchForm': form})
    info = searchDataP(form.cleaned_data['search'])
    return render(request, 'filter.html', {'info': info, 'searchForm': form})
"""


#2.Personas con su mismo CODELEC

#3. Personas con su mismo CODELEC por sexo


#CONSULTAS
#1. cantidad de todos los votantes

def getQuantityVoters(request):
    #por Costa Rica
    quantity = Padron_electoral.objects.all().count()
    quantityF = Padron_electoral.objects.filter(sexo=2).count()
    quantityM = Padron_electoral.objects.filter(sexo=1).count()
    #por provincia
    quantitySJ = Padron_electoral.objects.filter(Q(codelec__startswith='1')).count()
    quantityMSJ = Padron_electoral.objects.filter(Q(codelec__startswith="1")& Q(sexo=2)).count()
    quantityHSJ = Padron_electoral.objects.filter(Q(codelec__startswith="1")& Q(sexo=1)).count()
    quantityA = Padron_electoral.objects.filter(Q(codelec__startswith='2')).count()
    quantityMA = Padron_electoral.objects.filter(Q(codelec__startswith='2')& Q(sexo=2)).count()
    quantityHA = Padron_electoral.objects.filter(Q(codelec__startswith='2') & Q(sexo=1)).count()
    quantityC = Padron_electoral.objects.filter(Q(codelec__startswith='3')).count()
    quantityMC = Padron_electoral.objects.filter(Q(codelec__startswith='3')& Q(sexo=2)).count()
    quantityHC = Padron_electoral.objects.filter(Q(codelec__startswith='3')& Q(sexo=1)).count()
    quantityH = Padron_electoral.objects.filter(Q(codelec__startswith='4')).count()
    quantityMH = Padron_electoral.objects.filter(Q(codelec__startswith='4')& Q(sexo=2)).count()
    quantityHH = Padron_electoral.objects.filter(Q(codelec__startswith='4')& Q(sexo=1)).count()
    quantityG = Padron_electoral.objects.filter(Q(codelec__startswith='5')).count()
    quantityMGu = Padron_electoral.objects.filter(Q(codelec__startswith='5')& Q(sexo=2)).count()
    quantityHGu = Padron_electoral.objects.filter(Q(codelec__startswith='5')& Q(sexo=1)).count()
    quantityP = Padron_electoral.objects.filter(Q(codelec__startswith='6')).count()
    quantityMP = Padron_electoral.objects.filter(Q(codelec__startswith='6')& Q(sexo=2)).count()
    quantityHP = Padron_electoral.objects.filter(Q(codelec__startswith='6')& Q(sexo=1)).count()
    quantityL = Padron_electoral.objects.filter(Q(codelec__startswith='7')).count()
    quantityML = Padron_electoral.objects.filter(Q(codelec__startswith='7')& Q(sexo=2)).count()
    quantityHL = Padron_electoral.objects.filter(Q(codelec__startswith='7')& Q(sexo=1)).count()

    return render(request, 'generic.html', context={"quantity": quantity, "quantityFG": quantityF, "quantityMG": quantityM,
                                                    "quantitySJ":quantitySJ, "quantityMSJ": quantityMSJ, "quantityHSJ": quantityHSJ,
                                                    "quantityA": quantityA,"quantityMA": quantityMA,"quantityHA": quantityHA,
                                                    "quantityC": quantityC,"quantityMC": quantityMC,"quantityHC": quantityHC,
                                                    "quantityH": quantityH,"quantityMH": quantityMH,"quantityHH": quantityHH,
                                                    "quantityG": quantityG,"quantityMGu": quantityMGu,"quantityHGu": quantityHGu,
                                                    "quantityP": quantityP,"quantityMP": quantityMP,"quantityHP": quantityHP,
                                                    "quantityL": quantityL,"quantityML": quantityML,"quantityHL": quantityHL,})
