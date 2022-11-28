# historic_cities_django
A Django application showing the growth and location of historical cities based on the Urban Spatial Data from 3700BC to 2000AD found at https://sedac.ciesin.columbia.edu/data/set/urbanspatial-hist-urban-pop-3700bc-ad2000, and is a copy of a version done in ruby at https://github.com/scharlau/historical_cities.



Use xlrd to parse excel sheet https://www.oreilly.com/library/view/data-wrangling-with/9781491948804/ch04.html - but this only reads xls files, so switched to https://openpyxl.readthedocs.io/en/stable/ which proved very fast for the 10k plus records.

Use manage.py dbshell to confirm records are in the sqlite database.

Given so many records, we need to use pagination: https://docs.djangoproject.com/en/4.1/topics/pagination/

Things to try:
1. organise cities by country
2. Add chart showing population for each city.
3. Add map showing location of each city.

Step 1) We'll use location of historical cities based on the Urban Spatial Data from 3700BC to 2000AD found at https://sedac.ciesin.columbia.edu/data/set/urbanspatial-hist-urban-pop-3700bc-ad2000, which you can save to somewhere on your device. This gives us plenty of interesting things that we can do with the data.

Save the file, open it, and make these two changes to an entry so that it doesn't cause issues later: The spreadsheet has one row with a slash '/' in the name, which causes problems, so search for Frankfurt/Oder and change it to 'Frankfurt am Oder' in the name, and 'Frankfurt_am_Oder...' in the cityid. Then save the file again.

#### Table Relationships for the Data

We are not using all of the columns that are here. We could use all of the data, but we don't need the row id, as we'll create our own, and we don't need the 'certainty' measure either, so we'll ignore those. You can see the table structure in the parse_cities.py file where we create the table.

Step 2) We can start developing our application to display the data. Create a new project folder called 'polar_bears' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.10.7 # this sets the local version of python to 3.10.7
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

And that will install django version 4.x (or newer) with its associated dependencies. We can now start to build the application.

Now we can start to create the site using the django admin tools. Issue this command, and don't forget the '.' at the end of the line, which says 'create it in this directory'. This will create the admin part of our application, which will sit alongside the actual site. 

        django-admin startproject historic_cities .

We're using the name 'historic_cities' but you could use whatever seems appropriate. We'll save the 'cities' label for later in the app. For now we're setting up the support structure for the site, which will live in a separate folder.

We need to specify some settings for the site, which we do in the historic_cities/settings.py file. Open this and add this line above the line for pathlib import Path:

        import os

Now go to the end of the file to add a line specifying the root directory for the static files.

        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Now go further up the file to 'ALLOWED_HOSTS' so that we can run this beyond 'localhost' and 127.0.0.1, which are the only allowed ones if this is empty. Modify this accordingly to suit your needs:

        ALLOWED_HOSTS = ['localhost']

We now need to configure the database, which you saw was already detailed in the settings.py file. As django has a built-in admin tool, it already knows some of the tables that it needs to use. We can set this up with the command:

        python3 manage.py migrate

You should see a number of steps being run, each hopefully ending ... OK
If not, then look to the errors in the terminal. If you see one that says 'NameError: name 'os' is not defined', then go back and add the import for the 'os' library.

## Start the Server

We so this using the manage.py command tool by entering this command in the terminal:

        python3 manage.py runserver

If you're doing this on another platform, then you might need to use this instead (change the port number from 8000 as required):

        python3 manage.py runserver 0.0.0.0:8000 

If it went well, then you should see the python rocket launching your site. 

## Modelling our Data
The goal is to have the polar bear details on the website, which means we need to put the spreadsheet data into a database. This means creating models that map to tables in the database using Django's object relational mapping library.

We can now set about creating the space for our polar bear content by running this command:

        python3 manage.py startapp cities

This will create a new folder 'cities' containing relevant config files for us including space for database migrations, and other details specific to our content. 

Inside the 'cities' folder create a new folder called 'city_data'. We can now take the downloaded city data and put the 'urbanspatial-hist-urban-pop-3700bc-ad2000-xlsx' file into the 'city_data' folder. We'll need this later when we load the data into the database.

We need to modify the settings.py file in the historic_cities app, so that it knows to include the 'cities' contents. We do this by adding a line in the section on 'INSTALLED_APPS'. Add this line to the end of the block ( plus the , at the end of the line above it).

        'cities',

Now we can open 'cities/models.py' and start adding the schema for our tables. We'll start by adding a model for the cities. There is a lot of info in the spreadsheet file, but we'll only focus on the basic attributes. We label all of the attributes with a lower-case letter so that if (when) we move this to a different database, such as Postgresql, or MySQL, we don't have issues with columns starting with capital letters. Add the missing lines so that your file looks like this:

        from django.db import models
        from django.conf import settings

        # Create your models here.

        class City(models.Model):
            id = models.BigAutoField(primary_key=True)
            city = models.TextField()
            otherName = models.TextField()
            country = models.TextField()
            latitude = models.FloatField()
            longitude = models.FloatField()
            year = models.IntegerField()
            pop = models.IntegerField()
            city_id = models.TextField()

            def __str__(self):
                return f'{self.id}, {self.city}, {self.otherName}, {self.country}, {self.latitude},{self.longitude}, {self.year}, {self.pop}, {self.city_id}'

Now we nee to generate a migration file for Django to use when it loads the model into the schema. By having Django do this, it will generate the correct SQL needed for our database. The timestamp will be generated automatically for us for each new entry.

First, we ask Django to generate the migration file with the command:

        python3 manage.py makemigrations cities

This will read the models.py file and generate a migration file based on changes found there. 

Second, we run the generated migration with the command:

        python3 manage.py migrate cities

 In the future, anytime that you edit the model, you need to run makemigration, and then migrate commands to have the database changes happen.

Now we have the migration done and the table is created in our database, and we can load our data into the database. We do this using Django's admin commands, which provide access to the models, and thus the database for us. See more here: https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/ 

Under the 'cities' app create a folder 'management' and inside that create another one named 'commands'. Then create a file parse_cities.py in that folder. We use the openpyxl library to parse the excel spreadsheet, so you need to install that with the command:

        pip install openpyxl

With that in place we can now use the city model to help us import the spreadsheet data. There are a few interesting points to note here:
a) we drop the table objects, so that we can run this repeatedly, and not duplicate entries.
b) we use paths, and relative ones, so that we don't need to know where this application sits on the file system, but will always work.
c) as the openpyxl library goes cell by cell, we need to iterate over each cell in a row and check its column name to know which cell we're parsing so that we can assign it the correct variable name in order to create a new 'city' to save in the database.
d) the print statements are there to track progress.

Put this code into that file:

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

                # placeholder variables for city object
                city = "temp_name"
                otherName = "None"
                country = "temp_country"
                latitude = 0.0
                longitude = 0.0
                year = 1111
                pop = 111
                city_id = "temp_id"

                # as this is a spreadsheet and not a csv file, we need to iterate cell by cell over a range of cells
                # skip first row as headers, and skip first column as we don't need it
                for i in range(2, max_row_num+1):

                    for j in range(2, max_col_num+1):
                        cell_obj=sheet.cell(row=i, column=j)
                        if cell_obj.column_letter=='B':
                            city = cell_obj.value
                        if cell_obj.column_letter=='C':
                            if cell_obj.value is not None:
                                otherName = cell_obj.value
                        if cell_obj.column_letter=='D':
                            country = cell_obj.value
                        if cell_obj.column_letter=='E':
                            latitude = cell_obj.value
                        if cell_obj.column_letter=='F':
                            longitude = cell_obj.value
                        if cell_obj.column_letter=='H':
                            year = cell_obj.value
                        if cell_obj.column_letter=='I':
                            pop = cell_obj.value
                        if cell_obj.column_letter=='J':
                            city_id = cell_obj.value
                        
                        print(cell_obj.value, end='|')
                    # end loop so construct city object
                    city = City.objects.create(city=city,otherName=otherName,country=country,latitude=latitude,longitude=longitude,year=year,pop=pop,city_id=city_id)
                    city.save()
                    print(' saved ')
                    print('\n')

With this we can drop the data from the table, and then load it in, as required. We don't use any libraries for this as we want to pull specific fields from the file. Run the file with the command:

        python3 manage.py parse_cities

This should run fine.

## Creating Views
We can now create views for our data so that we can see all of the bears, plus also have a page to view details about each individual one.

Open historic_cities/urls.py and add 'include' to the import list, and add the second line as well below the one for 'admin.site.urls':

        from django.urls import path, include

        path('', include('cities.urls')),

This tells our application to look for content in the 'cities' app. 

Next go into the 'cities' folder and create an empty 'urls.py' file for us to manage the available views in the app. To start with put this into the file:

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.city_list, name='city_list'),
            path('cities/<str:city>', views.city__by_name, name='cityname'),
            ]

This provides us with the urls for two paths: one to show all of the cities, and another to show us the list of entries for a specific city name. The <str:city> part says the parameter called 'city' takes a string and then returns the view 'city_by_name', which we'll add in a moment.

We can now open 'cities/views.py' to add the view methods to generate a list of cities.

        from django.core.paginator import Paginator
        from django.shortcuts import render
        from .models import City

        # Create your views here.
        def city_list(request):
            cities = City.cities()
            paginator = Paginator(cities, 50) #show 50 cities per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'cities/city_list.html', {'page_obj': page_obj})

        def city__by_name(request, city):
            cities = City.city_by_name(city)
            paginator = Paginator(cities, 50) #show 50 cities per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'cities/city_list.html', {'page_obj': page_obj})

Our two views reuse the same html file for simplicity. Both also rely upon methods in the City class, in order to keep more code tied to cities there, instead of putting it into the view. Add these two methods to the cities/models.py file:

        def cities():
            cities = City.objects.all()
            return cities
        
        def city_by_name(city):
            city_list = City.objects.filter(city=city)
            return city_list



Next, we need to create the actual html page to display our cities. We'll put folders in the place that Django looks for them, which seems like extra work, but is convention. 

As before, create a 'templates' folder under 'cities' and then another 'cities' folder under that. Then create a file at 'cities/templates/cities/city_list.html' which has this simple code:
       
       <html><head>
       <title>Historic Cities</title>
        </head><body>
            <h1>Historic Cities</h1>
            {% for city in page_obj %}
            <b> <a href={% url 'cityname' city=city.city %}>{{city.city }}</a></b>
            This is {{ city.city }} also sometimes known as {{ city.otherName }} in 
            {{city.country}}, with the {{ city.pop }} in {{ city.year }}, and located at 
            {{ city.latitude }} and {{ city.longitude }}
            </p>
            {% endfor %}
            
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}

                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </body></html>
 

This will show the full list of cities, and includes pagination so that we don't try to show all 10K plus entries at once. 

First, add a link to retrieve all entries for a city on the bear_list.html page around 'city' like this:

         <b> <a href="{% url 'cityname' city=city.city %}">{{ city.city }}</a></b>

This will link the city_list page to the city.city value (the name of the city), which we'll pass to the query for the page.

Second, this makes use of the line in cities/urls.py for the view, which asks for cities/<str:city>:

        path('cities/<str:city>', views.city__by_name, name='cityname'),

This tells the view to expect a string as 'city' to be used in the query.

Now you can reload the page, and you should be able to see the cities pages. 

Finally, we're ready to do some more work with this so that we can add the sightings from the other table and show them on the bear detail page.




