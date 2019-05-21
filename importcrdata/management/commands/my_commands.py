import threading
from django.core.management.base import BaseCommand
import time
from django.db import connection
from importcrdata.models import PadronElectoral, Distelec

class Command(BaseCommand):
    help = 'Fills the Database'

    def readDataFromFile(self):

        file1 = open("PADRON_COMPLETO.txt", encoding="latin-1")
        list_padron = []
        padron = []
        cantidad_registros = 0
        id = 1
        then = time.time()

        if True:
            for line in file1:

                newLine = line.split(',')
                newLine[-1] = newLine[-1].split(' ')[0]

                padron.append((id, newLine[0], newLine[1], newLine[2], newLine[3], newLine[4],
                                         newLine[5].strip() + ' ' + newLine[6].strip() + ' ' + newLine[7]))

                x += 1
                id += 1
                if x == 10000:


                    print('nuevo')
                    print(x)
                    yield padron
                    x = 0
                    padron = []

        if padron:
            yield padron

        now = time.time()
        print("It took: ", now - then, " seconds")

    def loadDataToDatabase(self):
        for x in self.readDataFromFiles():

            print('hola')
            # print(x)

            # PadronElectoral.objects.bulk_create(x)
            then = time.time()
            query = "INSERT INTO importcrdata_padronelectoral (id, cedula, codele, sexo, fechacaduc, junta, nombre_completo) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.executemany(query, x)

            print("Se han creado 10 000 registros")
            now = time.time()
            print("10 000 records, took: ", now - then, " seconds")

    def handle(self, *args, **kwargs):
        x = threading.Thread(target=self.loadDataToDatabase)
        x.start()