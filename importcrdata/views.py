from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin, CreateView

from importcrdata.forms import SearchForm,SearchLocationForm,SearchCantonForm
from tse_demo.settings import BASE_DIR
import os
from importcrdata.models import PadronElectoral,Distelec

from . import forms
import re
# Create your views here.
import logging
import queue
import threading

import time
from importcrdata.decorators import is_request_param

def typeValidator(data,fn):
    try:
        result = fn(data)
        return result
    except:
        return 'error'

def tsePaginator(search_name,type):
    if type == 'int':
        if len(search_name) == 6: #i
            temp_data = PadronElectoral.objects.filter(codelec__icontains=str(search_name))

            if len(temp_data) == 0:
                temp_data = PadronElectoral.objects.filter(cedula__icontains=str(search_name))
            # temp_page = page
            # temp_paginator = Paginator(temp_data, 5)
        else:
            temp_data = PadronElectoral.objects.filter(cedula__icontains=str(search_name))
            # temp_page = page
            # temp_paginator = Paginator(temp_data,5)

        # try:
        #     temp_datas = temp_paginator.page(temp_page)
        # except PageNotAnInteger:
        #     temp_datas = temp_paginator.page(1)
        # except EmptyPage:
        #     temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return temp_data
    elif type == 'str':
        temp_data = PadronElectoral.objects.filter(nombre__icontains=str(search_name))
        temp_data2 = PadronElectoral.objects.filter(apellido1__icontains = str(search_name))
        temp_data3 = PadronElectoral.objects.filter(apellido2__icontains=str(search_name))
        #temp_page = page
        whole_data = temp_data | temp_data2 | temp_data3
        # temp_paginator = Paginator(whole_data, 5)
        #
        # try:
        #     temp_datas = temp_paginator.page(temp_page)
        # except PageNotAnInteger:
        #     temp_datas = temp_paginator.page(1)
        # except EmptyPage:
        #     temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return whole_data
    elif type == 'init':
        temp_data = PadronElectoral.objects.all()
        # temp_page = page
        # temp_paginator = Paginator(temp_data, 5)
        #
        # try:
        #     temp_datas = temp_paginator.page(temp_page)
        # except PageNotAnInteger:
        #     temp_datas = temp_paginator.page(1)
        # except EmptyPage:
        #     temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return temp_data

# def getTseData(request):
#     form = forms.SearchForm()
#
#     if request.method == 'POST':
#         form = forms.SearchForm(request.POST)
#         if form.is_valid():
#             if form.cleaned_data['search_name'] != '':
#                 if typeValidator(form.cleaned_data['search_name'], int) != 'error':
#                     padrones = tsePaginator(form.cleaned_data['search_name'], 'int', request.GET.get('page', 1))
#
#                 elif typeValidator(form.cleaned_data['search_name'], str) != 'error':
#                     padrones = tsePaginator(form.cleaned_data['search_name'], 'str', request.GET.get('page', 1))
#
#         return render(request, 'test.html', {'padrones': padrones, 'searchForm': form})
#
#     padrones = tsePaginator('', 'init', request.GET.get('page', 1))
#
#     return render(request, 'test.html', {"padrones": padrones, 'searchForm': form})

# def get_voters_location(option,loc_name):
#     ''' you can use this for get the statistics by province, canton or distric, pasong option like filter and the location name '''
#     if option == 'province':
#         province_info = PadronElectoral.objects.filter(provi)
#     elif option == 'canton':
#
#     elif option == 'distric':
#
#     return None


def get_global_statistics(fechacaduc):

    '''
    :param fechacaduc: // you can use this to get statistics like voters that id caducate the same day as president id.  and others.
    :return:
    '''
    total_male_voters = PadronElectoral.objects.filter(sexo=1).count()
    total_female_voters = PadronElectoral.objects.filter(sexo=2).count()
    caduc_voters = PadronElectoral.objects.filter(fechacaduc=fechacaduc).count()

    return  {'caduc':caduc_voters,'males':total_male_voters, 'females': total_female_voters}


def get_voters_same_name_count(name, codelec):
    '''   You can use this function to get specific voters that share the same name.  '''

    count_same_name = PadronElectoral.objects.filter(Q(nombre=name) & Q(codelec=codelec)).count()
    return {'same_name':count_same_name}

def get_voters_count(codelec):
    ''' You can use this function to retrieve male,female,and the total of voters of padron electoral  '''

    count_male = PadronElectoral.objects.filter(Q(codelec=codelec) & Q(sexo= 1)).count()
    count_female = PadronElectoral.objects.filter(Q(codelec=codelec) & Q(sexo=2)).count()
    count_voters = PadronElectoral.objects.filter(Q(codelec=codelec)).count()

    return {'male': count_male, 'female': count_female, 'total': count_voters}

class ElectorInfoView(DetailView):
    model = PadronElectoral
    template_name = 'info.html'
    context_object_name = 'elector_data'


    def get_context_data(self, **kwargs):
        context = super(ElectorInfoView,self).get_context_data(**kwargs)
        form = SearchForm
        if kwargs['object'] != None:
            distelec_info = Distelec.objects.get(codelec = kwargs['object'].codelec.codelec)
            context['distelec_info'] = distelec_info
            context['voters'] = get_voters_count(kwargs['object'].codelec.codelec)
            context['voters_same_name'] = get_voters_same_name_count(kwargs['object'].nombre, kwargs['object'].codelec.codelec)
        print(context)
        context['form'] = form

        return context


    def get_object(self):
        cedula_ = self.kwargs.get('cedula')

        try:
            data = PadronElectoral.objects.get(cedula=cedula_)
        except PadronElectoral.DoesNotExist:
            data = None

        return data


class Statistics(DetailView):
    model = PadronElectoral
    template_name = 'statistics.html'



    def get_context_data(self, **kwargs):
        context = super(Statistics, self).get_context_data(**kwargs)
        if kwargs['object'] != None:
            cad_voters_count = PadronElectoral.objects.filter(fechacaduc=kwargs['object'].fechacaduc).count()
            context['caduc_voters'] = cad_voters_count

        context['pform'] = SearchLocationForm

        if self.request.GET:
            if self.request.GET.get('option') == 'province':

                # cantons = list(Distelec.objects.filter(codelec__startswith= self.request.GET.get('province_id')).distinct('canton'))
                #
                # foo_list = []
                # for canton in cantons:
                #    foo_list.append({canton.codelec,canton.canton},)
                #
                cform = SearchCantonForm()

                print(cform)
                context['form'] = cform

        print(context)
        return context

    def get_object(self):

        try:
            data = PadronElectoral.objects.get(cedula='110600078')
        except PadronElectoral.DoesNotExist:
            data = None

        return data


class PadronView(ListView):

    template_name = 'test.html'
    paginate_by = 10
    context_object_name = 'padrones'


    def get_queryset(self):

        if self.request.GET.get('search_name'):
            search_name = self.request.GET.get('search_name')
            print(search_name)
            if typeValidator(search_name, int) != 'error':
                data = tsePaginator(search_name, 'int')

            elif typeValidator(search_name, str) != 'error':
                data = tsePaginator(search_name, 'str')

            return data
        else:
            data = PadronElectoral.objects.all()

            return data


    def get_context_data(self,*args, **kwargs):
        context = super(PadronView, self).get_context_data(**kwargs)
        print(context)
        context['form'] = SearchForm()

        return context

class NewPerson(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': SearchLocationForm()}
        return render(request, 'books/book-create.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = SearchLocationForm(request.POST)
    #     if form.is_valid():
    #         padron = form.save()
    #         padron.save()
    #         return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
    #     return render(request, 'books/book-create.html', {'form': form})

    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(user=self.user, title=title).exists():
            raise forms.ValidationError("You have already written a book with same title.")
        return title