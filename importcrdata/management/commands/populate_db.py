from django.core.management.base import BaseCommand
from importcrdata.models import PadronElectoral, Distelec
from django.db import connection
import argparse
import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fills the Padron Electoral Table'

    def add_arguments(self, parser):
        """
        Command will need 2 params to work, the Padron_Completo and Distelec.txt path.

        argparse library allow to load a file directly. More info: https://docs.python.org/3.3/library/argparse.html

        """

        parser.add_argument('distelec', type=argparse.FileType('r', encoding="ISO-8859-1"),
                            help='Path to Distelec.txt')
        parser.add_argument('padron', type=argparse.FileType('r', encoding="ISO-8859-1"),
                            help='Path to PADRON_COMPLETO.txt')

        logger.info("Distelec.txr file loaded to system.")
        logger.info("PADRON_COMPLETO.txr file loaded to system.")

    def clean_tables(self):
        """
        Delete all data on database if exists.
        """
        print("Deleting Distelect & Padron Electoral data")
        distelec_records = Distelec.objects.all().count()
        Distelec.objects.all().delete()
        print('Records de Distelect borrados: ', distelec_records)
        padron_records = PadronElectoral.objects.all().count()
        PadronElectoral.objects.all().delete()
        print('Records de Padron Electoral borrados: ', padron_records)
        logger.info("Cleanup tables (Distelec & Padron Electoral)")

    def loadPadronElectoral(self, **options):
        """
        Recieves the options param whom contains the Padron file.
        """
        for lote in self.readDataFromPadronElectoral(options['padron']):
            then = time.time()
            PadronElectoral.objects.bulk_create(lote)
            now = time.time()
            t = then - now
            if len(lote) != 0:
                logger.info("%s records inserted to Padron Electoral Table, in %s seconds" %(len(lote), t))
            else:
                logger.info(" %int records added in total to Padron Electoral Table.", PadronElectoral.objects.count())

    def loadDistelect(self, **options):
        """
        Recieves the options param whom contains the Distelec file.
        """
        for lote in self.readDataFromDistelec(options['distelec']):
            then = time.time()
            Distelec.objects.bulk_create(lote)
            now = time.time()
            t=then - now
            if len(lote) != 0:
                logger.info("%s records inserted to Distelec Table, in %s seconds." %(len(lote), t))
            else:
                logger.info("%s records added in total to Distelec Table", Distelec.objects.count())

    def readDataFromPadronElectoral(self, padron):
        """
        Manipulates the PadronELectoral's file, it's in charge of split all the document and join it as a PadronElectoral object.
        It works in 10 000 batch size.
        """

        list_padron = []
        cantidad_registros = 0
        then = time.time()

        for line in padron:

            newLine = line.split(',')
            newLine[-1] = newLine[-1].split(' ')[0]

            list_padron.append(
                PadronElectoral(cedula=newLine[0], codele=newLine[1], sexo=newLine[2], fechacaduc=newLine[3],
                                junta=newLine[4],
                                nombre_completo=newLine[5].strip() + ' ' + newLine[6].strip() + ' ' + newLine[
                                    7].strip()))

            cantidad_registros += 1

            if cantidad_registros == 10000:
                yield list_padron
                cantidad_registros = 0
                list_padron = []

        if list_padron:
            yield list_padron

        now = time.time()
        yield []

        logger.info("Insert all data for Padron Electoral took: %s second", (now - then))

    def readDataFromDistelec(self, distelec):
        """
        Manipulates the Distelec's file, it's in charge of split all the document and join it as a PadronElectoral object.
        It works in 2000 batch size.
        """

        lista_distelec = []
        cantidad_registros = 0
        then = time.time()

        for line in distelec:

            newLine = line.split(',')
            newLine[-1] = newLine[-1].split(' ')[0]

            lista_distelec.append(
                Distelec(codele=newLine[0], provincia=newLine[1], canton=newLine[2], distrito=newLine[3]))

            cantidad_registros += 1

            if cantidad_registros == 2000:
                yield lista_distelec
                cantidad_registros = 0
                lista_distelec = []

        if lista_distelec:
            yield lista_distelec

        now = time.time()
        yield []

        logger.info("Insert all data for Distelec took: %second", (now - then))

    def handle(self, *args, **options):
        """
        Main method that call all the other instances.
        """
        self.clean_tables()
        self.loadDistelect(**options)
        self.loadPadronElectoral(**options)
