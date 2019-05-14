from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse
from tse_demo.settings import BASE_DIR
import os
from importcrdata.models import PatronElectoral,Distelec
from . import forms
import re
# Create your views here.
import logging
import queue
import threading

import time


def typeValidator(data,fn):
    try:
        result = fn(data)
        return result
    except:
        return 'error'

def tsePaginator(search_name,type,page):
    if type == 'int':
        if len(search_name) == 6: #i
            temp_data = PatronElectoral.objects.filter(codele__icontains=str(search_name))

            if len(temp_data) == 0:
                temp_data = PatronElectoral.objects.filter(cedula__icontains=str(search_name))
            temp_page = page
            temp_paginator = Paginator(temp_data, 5)
        else:
            temp_data = PatronElectoral.objects.filter(cedula__icontains=str(search_name))
            temp_page = page
            temp_paginator = Paginator(temp_data,5)

        try:
            temp_datas = temp_paginator.page(temp_page)
        except PageNotAnInteger:
            temp_datas = temp_paginator.page(1)
        except EmptyPage:
            temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return temp_datas
    elif type == 'str':
        temp_data = PatronElectoral.objects.filter(nombre__icontains=str(search_name))
        temp_data2 = PatronElectoral.objects.filter(apellido1__icontains = str(search_name))
        temp_data3 = PatronElectoral.objects.filter(apellido2__icontains=str(search_name))
        temp_page = page
        whole_data = temp_data | temp_data2 | temp_data3
        temp_paginator = Paginator(whole_data, 5)

        try:
            temp_datas = temp_paginator.page(temp_page)
        except PageNotAnInteger:
            temp_datas = temp_paginator.page(1)
        except EmptyPage:
            temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return temp_datas
    elif type == 'init':
        temp_data = PatronElectoral.objects.all()
        temp_page = page
        temp_paginator = Paginator(temp_data, 5)

        try:
            temp_datas = temp_paginator.page(temp_page)
        except PageNotAnInteger:
            temp_datas = temp_paginator.page(1)
        except EmptyPage:
            temp_datas = temp_paginator.page(temp_paginator.num_pages)
        return temp_datas



def getTseData(request):
    form = forms.SearchForm()

    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['search_name'] != '':
                if typeValidator(form.cleaned_data['search_name'], int) != 'error':
                    padrones = tsePaginator(form.cleaned_data['search_name'], 'int', request.GET.get('page', 1))

                elif typeValidator(form.cleaned_data['search_name'], str) != 'error':
                    padrones = tsePaginator(form.cleaned_data['search_name'], 'str', request.GET.get('page', 1))

        return render(request, 'test.html', {'padrones': padrones, 'searchForm': form})

    padrones = tsePaginator('', 'init', request.GET.get('page', 1))

    return render(request, 'test.html', {"padrones": padrones, 'searchForm': form})
my_queue = queue.Queue()
def storeInQueue(f):

    def wrapper(*args):
        my_queue.put(f(*args))
    return wrapper

@storeInQueue
def loadDataToBd():

       file1 = open("PADRON_COMPLETO.txt", encoding="latin-1")
       lines = []
       x=0
       then = time.time()
       for line in file1:
           newLine = re.sub(' +|\n', ' ', line)
           newLine = newLine.split(',')
           newLine[-1] = newLine[-1].split(' ')[0]
           lines.append(newLine)
           PatronElectoral.objects.create(cedula=newLine[0], codele=newLine[1], sexo=newLine[2], fechacaduc=newLine[3], junta=newLine[4], nombre=newLine[5], apellido1=newLine[6], apellido2=newLine[7])
           x = x + 1.

       now = time.time()

       print("It took: ", now-then, " seconds")

def loadDataView(request):
    x = threading.Thread(target=loadDataToBd)
    x.start()
    my_queue = queue.Queue()
    my_data = my_queue.get()

    return render(request, 'test.html', context = {'data': my_data})


