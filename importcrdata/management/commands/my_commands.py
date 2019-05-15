from django.core.management.base import BaseCommand
from django.db import connection
from contextlib import closing

import threading
import time
import re

class Command(BaseCommand):
    help = 'Loading data to Database.'

    def handle(self, *args, **kwargs):
        x = threading.Thread(target=self.readDataFromFile)
        x.start()

    def readDataFromFile(self):
        file1 = open("PADRON_COMPLETO.txt", encoding="latin-1")
        padron_electoral = []
        id_registro = 1
        numero_registros = 1
        then = time.time()
        for line in file1:
            newLine = re.sub(' +|\n', ' ', line)
            newLine = newLine.split(',')
            newLine[-1] = newLine[-1].split(' ')[0]

            padron_electoral.append((id_registro, newLine[0], newLine[1], newLine[2], newLine[3], newLine[4], newLine[5], newLine[6], newLine[7]))

            id_registro += 1
            numero_registros += 1

            if (numero_registros == 4000):
                values = tuple(padron_electoral)

                query = "INSERT INTO importcrdata_padronelectoral (id, cedula, codele, sexo, fechacaduc, junta, nombre, apellido1, apellido2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                with closing(connection.cursor()) as cursor:
                    cursor.executemany(query, values)

                print("Se han creado 4000 registros, total de registros: ",id_registro)
                padron_electoral.clear()
                numero_registros = 0


        now = time.time()

        print("It took: ", now - then, " seconds")