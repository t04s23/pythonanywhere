# historic_cities_django
A Django application showing the growth and location of historical cities based on the Urban Spatial Data from 3700BC to 2000AD found at https://sedac.ciesin.columbia.edu/data/set/urbanspatial-hist-urban-pop-3700bc-ad2000, and is a copy of a version done in ruby at https://github.com/scharlau/historical_cities.

Spreadsheet has one row with / in the name, which causes problems, so search for Frankfurt/Oder and change it to 'Frankfurt am Oder' in the name, and 'Frankfurt_am_Oder...' in the cityid.

Use xlrd to parse excel sheet https://www.oreilly.com/library/view/data-wrangling-with/9781491948804/ch04.html - but this only reads xls files, so switched to https://openpyxl.readthedocs.io/en/stable/ which proved very fast for the 10k plus records.

Use manage.py dbshell to confirm records are in the sqlite database.

Given so many records, we need to use pagination: https://docs.djangoproject.com/en/4.1/topics/pagination/

Things to try:
1. organise cities by country
2. Add chart showing population for each city.
3. Add map showing location of each city.



