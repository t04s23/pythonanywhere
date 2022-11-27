from django.urls import path
from . import views

urlpatterns = [
    path('', views.city_list, name='city_list'),
    path('cities/<str:city>', views.city__by_name, name='cityname'),
    ]