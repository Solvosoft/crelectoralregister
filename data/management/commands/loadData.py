from django.core.management.base import BaseCommand, CommandError
from data.models import Padron_electoral, Distelec
import time
import threading
import re

class Command(BaseCommand):
    help='Loading data'

    def add_arguments(self, parser):
        parser.add_argument('txt_file', type=str, help='File name:')

    def loadDataBD(self, fileName):
        #parser.add_argument('registry', type=argparse.FileType('r', encoding="ISO-8859-1"),help='Path to PADRON_COMPLETO.txt')
        fileComplete = open(fileName, encoding="latin-1")
        cont = 0
        then = time.time()
        list_padron = []
        if fileName == 'PADRON_COMPLETO.txt':
            for line in fileComplete:
                newL = re.sub(' +|\n', ' ', line)
                newL = newL.split(',')
                newL[-1] = newL[-1].split(' ')[0]
                list_padron.append(Padron_electoral(cedula=newL[0], codelec=newL[1], sexo=newL[2], fecha_caducidad=newL[3],
                                                    junta=newL[4], nombre=newL[5], primer_apellido=newL[6],
                                                    segundo_apellido=newL[7]))
                cont += 1
                if cont == 100:
                    yield list_padron
                    cont = 0
                    list_padron = []

        if fileName == 'Distelec.txt':
            for line in fileComplete:
                newL = re.sub(' +|\n', ' ', line)
                newL = newL.split(",")
                #newL[-1] = newL[-1].split(' ')

                Distelec.objects.create(codele=newL[0], provincia=newL[1], canton=newL[2], distrito=newL[3])
                cont += 1

                if cont == 100:
                    yield list_padron
                    cont = 0
                    list_padron = []
                    list_padron.clear()

        if list_padron:
            yield list_padron

        yield []
        now = time.time()
        print("Time: ", now - then, " seconds")

        fileComplete.close()

    def loadViewData(self, txt):
        for line in self.loadDataBD(txt):
            Padron_electoral.objects.bulk_create(line)
            #Distelec.objects.bulk_create(line)

    """def loadViewDistelec(self, txt):
        for line in self.loadDataBD(txt):
            Distelec.objects.bulk_create(line)"""

    def handle(self, *args, **kwargs):
        file = kwargs['txt_file']
        #self.loadViewData(file)
       # self.loadViewDistelec(file)
        #self.loadDataBD(file)
        threadFile = threading.Thread(target=self.loadViewData, args=(file,))
        threadFile.start()
        #threading.join()

    def deletePadronElectoral(self):
        deleteData = 'select'

#comando para eliminar o limpiar la bd pero no usar padron.objects.all().delete()
#eliminarlo con sql