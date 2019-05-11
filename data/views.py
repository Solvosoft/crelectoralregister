import os, re
from tse.settings import BASE_DIR
from django.shortcuts import render
from data.models import Padron_electoral
# Create your views here.



def getData(request):
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

