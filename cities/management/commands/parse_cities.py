import xlrd
import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError

from cities.models import City

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        City.objects.all().delete()
        print('table dropped')

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        book_path = os.path.join(base_dir, '/cities/city_data/urbanspatial-hist-urban-pop-3700bc-ad2000-xlsx.xlsx')
        book = xlrd.open_workbook(book_path)
        sheet = book.sheet_by_name('Historical Urban Population')
        print(sheet.nrows)