import argparse
import re
import threading

from django.core.management.base import BaseCommand
from django.utils import timezone
import time
import logging
from django.db import connection

from importcrdata.models import PadronElectoral,Distelec

import os
# Get an instance of a logger
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    ''' You can use this coomand for import the padron electoral and distelec data to the postgresql
        database,

        file_path :param
        options :param
            - distelec:param 'if you use this param, you indicate to load a Distelec file. muse use the correct file with the correct structure
            - padron:param 'use this, to load a padron electoral file, with the correct structure.
        '''
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('txt_file', type=argparse.FileType('r', encoding="ISO-8859-1"), help='path')
        parser.add_argument('option', type=str, help='path')

    def get_distelec(self,distelec):

        for ditelec_info in distelec:
            codelec,provincia,canton,distrito = ditelec_info.split(',')
            query = "INSERT INTO importcrdata_distelec values " + "('%s','%s','%s','%s');" % (codelec,provincia,canton,distrito.strip())
            yield query

    def get_padron(self,padron):

        query = ''
        cont = 0
        for padron_info in padron:
            cedula, codelec, sexo, fechacaduc, junta, nombre, apellido1, apellido2 = padron_info.split(',')
            query += 'INSERT INTO importcrdata_padronelectoral values' + "('%s','%s',%s,'%s','%s','%s','%s','%s');" % (cedula, codelec, sexo, fechacaduc,junta, nombre.strip().replace("'",' '), apellido1.strip().replace("'",' '), apellido2.strip().replace("'",' '))
            cont += 1
            if cont == 100000:
                yield query
                cont = 0
                query = ''
        if len(query) > 0:
            yield query


    def del_dist_registry(self):
        logger.error('Deleting distelec registry.')
        Distelec.objects.all().delete()
        logger.error('Distelec registry completed, ready to continue.')

    def del_padron_registry(self):
        logger.error('Deleting Padron Electoral registry.')
        PadronElectoral.objects.all().delete()
        logger.error('Padron Electoral deleted succesfully, ready to continue.')


    def in_bd(self,cursor,sql):
        then = time.time()
        cursor.execute(sql)
        logger.error('100.000 data saved into db.')
        now = time.time()
        print("It took: ", now - then, " seconds")

    def loadDataView(self, txt_file, *options):
        if options[0] == 'distelec':
            self.del_dist_registry()
            with connection.cursor() as cursor:
                logger.error('Iniciando con importacion a bd...')
                then = time.time()
                for x in self.get_distelec(txt_file):

                    z = threading.Thread(target=cursor.execute , args=(x,))
                    z.start()
                    z.join()

                now = time.time()
                print("It took: ", now - then, " seconds")
        if options[0] == 'padron':
            self.del_padron_registry()
            with connection.cursor() as cursor:
                logger.error('Iniciando de PADRON ELECTORAL, importacion a bd...')

                then = time.time()
                for x in self.get_padron(txt_file):

                    z = threading.Thread(target=self.in_bd, args=(cursor,x,))
                    z.start()
                    z.join()

                now = time.time()
                print("It took: ", now - then, " seconds")


    def handle(self, *args, **kwargs):
        logger.error('Iniciando con carga del archivo')
        option = kwargs['option']
        file_name = kwargs['txt_file']
        self.loadDataView(file_name,option)
        # x = threading.Thread(target=self.loadDataView, args=(file_name, option))
        # x.start()
        # x.join()




