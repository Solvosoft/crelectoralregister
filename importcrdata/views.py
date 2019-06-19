from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from importcrdata.decorators import validRequest
from django.views.generic import View, ListView, DetailView, CreateView
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from importcrdata.models import PadronElectoral, Distelec
from . import forms


class PadronView(ListView):
    """
    This is the main view, it contains the index.html file and it's in charge of display
    the padron electoral data.

    This view works with a param "q" in get requests that will help for filtering data.
    """
    template_name = 'importcrdata/index.html'

    #by default it goes inside this method and display the data based on "q" param.
    def get(self, request):

        form = forms.SearchForm()
        q = request.GET.get('q')

        if not q:
            padron_list = PadronElectoral.objects.all()
        else:
            searchType = self.getSearchType(q)
            if searchType:
                padron_list = self.filterBasedInNumberSearch(q)
            else:
                padron_list = PadronElectoral.objects.filter(nombre_completo__icontains=str(q))

        padron_paged = getListPaged(self, request, padron_list, 7)

        context = {'padron_paged': padron_paged, 'searchForm': form}
        return render(request, self.template_name, context)

    #Helper method that identifies if data is int or not.
    def getSearchType(self, search):
        try:
            int(search)
            return True
        except ValueError:
            return False

    #This method is in charge of filter the data only if it is a number.
    def filterBasedInNumberSearch(self, search):
        if len(search) == 6:
            return PadronElectoral.objects.filter(codele__iexact=str(search))
        else:
            return PadronElectoral.objects.filter(cedula__icontains=str(search))

class StatisticsView(View):
    """
    This view contains all the statistics data, its based on filters.
    """
    template_name = 'importcrdata/statistics.html'
    presidents_id = '110600078'

    def get(self, request):

        province_data = Distelec.objects.values('provincia').distinct()
        canton_data = Distelec.objects.values('provincia','canton').distinct()
        district_data = Distelec.objects.values('provincia','canton','distrito').distinct()

        self.total_of_people = PadronElectoral.objects.all().count()
        total_of_women = PadronElectoral.objects.filter(sexo=2).count()
        total_of_men = PadronElectoral.objects.filter(sexo=1).count()

        expiration_date_list = self.getPeopleInExpirationDate(self.presidents_id)
        expiration_list = getListPaged(self, request, expiration_date_list, 4)

        context = {'expiration_list': expiration_list,
                   'total_of_people': self.total_of_people,
                   'total_of_women': total_of_women,
                   'total_of_men': total_of_men,
                   'total_of_expirations': expiration_date_list.count(),
                   'province_data': province_data,
                   'canton_data':canton_data,
                   'district_data':district_data
                   }

        return render(request, self.template_name, context)

    def getPeopleInExpirationDate(self, id):
        date_param = PadronElectoral.objects.get(cedula__iexact=id)
        return PadronElectoral.objects.filter(fechacaduc__iexact=date_param.fechacaduc)

class PersonCreateView(ListView):
    """
    This view is a generic view used for add person to padron electoral.
    """
    template_name = 'importcrdata/add_person.html'

    def get(self, request):
        form = forms.PadronForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.PadronForm(request.POST)
        if form.is_valid():
            form.save()
        context = {'form': form}

        return redirect('importcrdata:index')

class ProvinciaAjaxView(ListView):
    """
    This view is in charge of display statistics by Province.
    """
    def get(self, request):

        province_id = request.GET['province_id']
        province_data = Distelec.objects.filter(provincia__iexact=province_id).values('codele')
        # The digit in position 0 contains the value for the province. That will help to filter
        province_identifier = province_data[0]['codele'][0]

        number_of_women = PadronElectoral.objects.filter(codele__startswith=province_identifier, sexo=2).count()
        number_of_men = PadronElectoral.objects.filter(codele__startswith=province_identifier, sexo=1).count()
        province_people = number_of_women + number_of_men

        return JsonResponse({'province_people': province_people, 'number_of_women': number_of_women, 'number_of_men': number_of_men})

class CantonAjaxView(ListView):
    """
    This view is in charge of display statistics by Canton.
    """
    def get(self, request):

        canton_id = request.GET['canton_id']
        ids_container = canton_id.split('-')
        provincia = ids_container[0]
        canton = ids_container[1]

        canton_data = Distelec.objects.filter(provincia__iexact=provincia, canton__iexact=canton).values('codele')
        #Joins the different codes to get a one who will work as a param to filter.
        canton_identifier = "".join([canton_data[0]['codele'][0], canton_data[0]['codele'][1], canton_data[0]['codele'][2]])


        number_of_women = PadronElectoral.objects.filter(codele__startswith=canton_identifier, sexo=2).count()
        number_of_men = PadronElectoral.objects.filter(codele__startswith=canton_identifier, sexo=1).count()
        province_people = number_of_women + number_of_men

        return JsonResponse({'province_people': province_people, 'number_of_women': number_of_women, 'number_of_men': number_of_men})

class DistritoAjaxView(ListView):
    """
    This view is in charge of display Distrito's statistics.
    """
    def get(self, request):

        district_id = request.GET['district_id']
        ids_container = district_id.split('-')

        provincia = ids_container[0]
        canton = ids_container[1]
        distrito = ids_container[2]

        district_data = Distelec.objects.filter(provincia__iexact=provincia, canton__iexact=canton, distrito__iexact=distrito).values('codele')
        #Joins the different codes to get a one who will work as a param to filter.
        district_identifier = "".join([district_data[0]['codele'][0], district_data[0]['codele'][1], district_data[0]['codele'][2], district_data[0]['codele'][3], district_data[0]['codele'][4], district_data[0]['codele'][5]])

        number_of_women = PadronElectoral.objects.filter(codele__startswith=district_identifier, sexo=2).count()
        number_of_men = PadronElectoral.objects.filter(codele__startswith=district_identifier, sexo=1).count()
        province_people = number_of_women + number_of_men

        return JsonResponse({'province_people': province_people, 'number_of_women': number_of_women, 'number_of_men': number_of_men})

class PadronDetailView(DetailView):
    """
    This view contains the profile for an specific user.
    """
    template_name = 'importcrdata/padron_detail.html'
    context_object_name = 'padron_detail'

    current_codele = ''
    full_name = ''

    def get_object(self):

        data = get_object_or_404(PadronElectoral, cedula=self.kwargs.get('cedula'))
        self.current_codele = data.codele
        self.full_name = data.nombre_completo
        return data

    # Data is filtered based on the codele of the selected person.
    def get_context_data(self, **kwargs):

        tempData = PadronElectoral.objects.filter(codele__iexact=str(self.current_codele))

        same_name = self.getPeopleWithSameName(self.full_name)
        number_of_women = tempData.filter(sexo=2)
        number_of_men = tempData.filter(sexo=1)

        return {'padron_detail': self.get_object(),
                'same_name': same_name,
                'number_of_women': len(number_of_women),
                'number_of_men': len(number_of_men)}

    # Method in charge of split the full name, compare it with the rest of people and return
    # the amount of people with the same name.
    def getPeopleWithSameName(self, name):

        tempData = PadronElectoral.objects.all()
        name_array = name.split(' ')

        if len(name_array) == 3:
            amount_of_people = 0
            name = name_array[0]
            tempData_filtered = tempData.filter(nombre_completo__istartswith=name)

            for data in tempData_filtered:
                current_name = data.nombre_completo.split(' ')
                if current_name[0] == name and len(current_name) == 3:
                    amount_of_people += 1

            return amount_of_people - 1

        elif len(name_array) == 4:
            name = ' '.join([name_array[0], name_array[1]])
            return len(tempData.filter(nombre_completo__icontains=name)) - 1

        else:
            name = ' '.join([name_array[0], name_array[1], name_array[2]])
            return len(tempData.filter(nombre_completo__icontains=name)) - 1

# Method in charge of paginate any list.
def getListPaged(self, request, list_for_paging, amount_per_page):
    paginator = Paginator(list_for_paging, amount_per_page)
    page = request.GET.get("page")

    try:
        list_paged = paginator.page(page)
    except PageNotAnInteger:
        list_paged = paginator.page(1)
    except EmptyPage:
        list_paged = paginator.page(paginator.num_pages)

    return list_paged

import csv
def generateCantonCSV(request, codigo):
    obj = PadronElectoral.objects.filter(codele__startswith=codigo)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="canton.csv"'
    writer = csv.writer(response)
    for y in obj:
        writer.writerow([y.codele, y.cedula, y.nombre_completo])
    return response

def efficientCantonCSV(request, codigo):
    obj = PadronElectoral.objects.filter(codele__startswith=codigo).values_list('codele', 'cedula', 'nombre_completo')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="canton.csv"'
    writer = csv.writer(response)
    writer.writerows(obj)
    return response

import django_excel as excel
def getCantonExcel(request, codigo):
    query_sets = PadronElectoral.objects.filter(codele__startswith=codigo)
    column_names = ['codele', 'cedula', 'nombre_completo']
    return excel.make_response_from_query_sets(
        query_sets,
        column_names,
        'xlsx',
        file_name="canton"
    )

import json
def getCantonJson(request, codigo):
    query_sets = PadronElectoral.objects.filter(codele__startswith=codigo).values('codele', 'cedula', 'nombre_completo')

    response = HttpResponse(json.dumps(list(query_sets)),content_type='text/json')
    # response['Content-Disposition'] = 'attachment; filename="canton.csv"'
    return response


def showJson(request):
    return render(request,'importcrdata/showjson.html', {})
# METHOD THAT TESTS A CUSTOM DECORATOR
@validRequest
def testDecorator(request):
    return render(request, 'importcrdata/test.html', {"context": 'context'})
