import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook

from cities.models import City

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        City.objects.all().delete()
        print('table dropped')

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        book_path = os.path.join(base_dir, 'cities/city_data/urbanspatial-hist-urban-pop-3700bc-ad2000-xlsx.xlsx')
        book = load_workbook(book_path)
        sheet = book['Historical Urban Population']
        print(sheet.title)
        max_row_num = sheet.max_row
        max_col_num = sheet.max_column
        print(max_row_num)
        print(max_col_num)

        # as this is a spreadsheet and not a csv file, we need to iterate cell by cell over a range of cells
        # skip first row as headers, and skip first column as we don't need it
        for i in range(2, max_row_num+1):
            for j in range(2, max_col_num+1):
                cell_obj=sheet.cell(row=i, column=j)
                print(cell_obj.value, end='|')
            print('\n')


            
        