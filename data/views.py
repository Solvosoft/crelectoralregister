import os, re
from tse.settings import BASE_DIR
from django.shortcuts import render
from data.models import Padron_electoral
from django.db.models import Count
# Create your views here.

#cargar los datos



def getAllData(request):
    """file = open(os.path.join(BASE_DIR, 'PADRON_COMPLETO.txt'))
    file1 = open("PADRON_COMPLETO.txt", encoding="latin-1")
    lines = []
    x=0
    for line in file1:
        newL = re.sub(' +|\n', ' ', line)
        newL = newL.split(',')
        newL[-1] = newL[-1].split(' ')[0]
        print(newL)
        lines.append(newL)

        Padron_electoral.objects.create(cedula=newL[0], codelec=newL[1], sexo=newL[2], fecha_caducidad=newL[3],
                                        junta=newL[4], nombre=newL[5], primer_apellido=newL[6], segundo_apellido=newL[7])
        x = x + 1
        if x == 10:
            break"""

    linea = Padron_electoral.objects.all()
    return render(request, 'test.html', {"data": linea})

#BUSQUEDA POR CEDULA
#1.Mostrar la info de la persona buscada
def getAllInfoByCedula(request):
    line = Padron_electoral.objects.all().filter(cedula="207000998")#recibir cedula desde pág
    print(line)
    return render(request, 'allInfo.html', {"dataByCedula": line})

#2.Personas con su mismo CODELEC

#3. Personas con su mismo CODELEC por sexo


#CONSULTAS
#1. cantidad de todos los votantes

def getQuantityVoters(request):
    quantity = Padron_electoral.objects.all().count()
    return render(request, 'generic.html', {"quantity": quantity})

#2. cantidad de mujeres y hombres votantes a nivel nacional
"""
def getQuantityVotersFemaleMaleCR(request):
    quantityF = Padron_electoral.objects.filter(sexo="2").count()
    return render(request, 'html', {"quantityF": quantityF})

def getQuantityVotersMaleMaleCR(request):
    quantityM = Padron_electoral.objects.filter(sexo="1").count()
    return render(request, 'html', {"quantityM": quantityM})
"""

#3. cantidad de mujeres y hombres votantes por provincia

#4. cantidad de mujeres y hombres votantes por canton

#4. cantidad de mujeres y hombres votantes por distrito