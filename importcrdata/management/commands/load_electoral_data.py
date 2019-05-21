import re
import threading

from django.core.management.base import BaseCommand
from django.utils import timezone
import time

from importcrdata.models import PadronElectoral,Distelec


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('txt_file', type=str, help='Indicates the file name:')

    def loadDataToBd(self,file_name):
        file1 = open(file_name, encoding="latin-1")
        list_padron = []
        x = 0
        then = time.time()
        if file_name == 'PADRON_COMPLETO.txt':
            for line in file1:
                newLine = re.sub(' +|\n', ' ', line)
                newLine = newLine.split(',')
                newLine[-1] = newLine[-1].split(' ')[0]

                list_padron.append(PadronElectoral(cedula=newLine[0], codelec=newLine[1], sexo=newLine[2], fechacaduc=newLine[3], junta=newLine[4], nombre=newLine[5], apellido1= newLine[6], apellido2=newLine[7]))
                x += 1

                if x == 10000:
                    yield list_padron
                    x = 0
                    list_padron = []

        elif file_name == 'Distelec.txt':
            for line in file1:
                newLine = re.sub(' +|\n', ' ', line)
                newLine = newLine.split(',')
                newLine[-1] = newLine[-1].split(' ')[0]

                Distelec.objects.create(codelec=newLine[0], provincia=newLine[1], canton=newLine[2], distrito=newLine[3])
                x += 1

                if x == 10000:
                    yield list_padron
                    x = 0
                    list_padron = []

        if list_padron:
            yield list_padron
        file1.close()
        now = time.time()
        yield []
        print("It took: ", now - then, " seconds")

    def loadDataView(self,txt_file):
         for x in self.loadDataToBd(txt_file):
            PadronElectoral.objects.bulk_create(x)


    def handle(self, *args, **kwargs):
        file_name = kwargs['txt_file']
        x = threading.Thread(target=self.loadDataView, args = (file_name,))
        x.start()
        x.join()



