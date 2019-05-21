from django.core.management.base import BaseCommand
from importcrdata.models import PadronElectoral, Distelec

import time

class Command(BaseCommand):
    help = 'Fills the Padron Electoral Table'

    def loadPadronElectoral(self):
        for lote in self.readDataFromPadronElectoral():
            then = time.time()
            PadronElectoral.objects.bulk_create(lote)
            now = time.time()
            print("10 000 records: ", now - then, " seconds")
            print("10 000 records have been inserted.")

    def loadDistelect(self):
        for lote in self.readDataFromDistelec():
            then = time.time()
            print('distelct')
            print(lote)
            Distelec.objects.bulk_create(lote)
            now = time.time()
            print("10 000 records: ", now - then, " seconds")


    def readDataFromPadronElectoral(self):

        file1 = open("PADRON_COMPLETO.txt", encoding="latin-1")
        list_padron = []
        cantidad_registros = 0
        then = time.time()


        for line in file1:

            newLine = line.split(',')
            newLine[-1] = newLine[-1].split(' ')[0]

            list_padron.append(PadronElectoral(cedula=newLine[0], codele=newLine[1], sexo=newLine[2], fechacaduc=newLine[3], junta=newLine[4], nombre_completo=newLine[5].strip() +' '+ newLine[6].strip()+' '+newLine[7].strip()))

            cantidad_registros += 1

            if cantidad_registros == 10000:
                yield list_padron
                cantidad_registros = 0
                list_padron = []

        if list_padron:
            yield list_padron

        now = time.time()
        yield []

        print("It took: ", now - then, " seconds")

    def readDataFromDistelec(self):

        file1 = open("Distelec.txt", encoding="latin-1")
        lista_distelec = []
        cantidad_registros = 0
        then = time.time()

        for line in file1:

            newLine = line.split(',')
            newLine[-1] = newLine[-1].split(' ')[0]

            lista_distelec.append(Distelec(codele=newLine[0], provincia=newLine[1], canton=newLine[2], distrito=newLine[3]))

            cantidad_registros += 1

            if cantidad_registros == 2000:
                yield lista_distelec
                cantidad_registros = 0
                lista_distelec = []

        if lista_distelec:
            yield lista_distelec

        now = time.time()
        yield []

        print("It took: ", now - then, " seconds")

    def handle(self, *args, **kwargs):
        self.loadDistelect()
        self.loadPadronElectoral()

