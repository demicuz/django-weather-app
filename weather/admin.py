from django.contrib import admin
from .models import City, CurrentWeather, CityStats

admin.site.register(City)
admin.site.register(CurrentWeather)
admin.site.register(CityStats)
