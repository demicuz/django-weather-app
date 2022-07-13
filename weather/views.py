from django.shortcuts import redirect, render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import City, CurrentWeather, create_current_weather
# from .forms import ShowCityForm

import requests

import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

def index(request):
    cities = City.objects.all()[:4]

    weather_data = []
    for city in cities:
        # TODO DRY, see city_detail()
        current_weather_set = CurrentWeather.objects.filter(city=city)

        if not current_weather_set:
            current_weather = create_current_weather(city, city.openweather_id)
        else:
            current_weather = current_weather_set[0]

        if not current_weather.was_updated_last_minute():
            current_weather.update()

        weather_data.append(current_weather)

    # show_city_form = ShowCityForm()
    # context = {'weather_data': weather_data, 'form': show_city_form}
    context = {'weather_data': weather_data, 'now': timezone.now()}

    return render(request, 'weather/index.html', context)

# TODO if/else mess...
# TODO could probably be a form. `render()` is totally incorrect here. Should
# redirect instead.
def view_city(request):
    city_name = request.POST['city_name']
    if not city_name:
        return render(request, 'weather/index.html', {
            'error_message': 'Search field is empty!'
        })

    city_set = City.objects.filter(name__iexact=city_name)
    if not city_set:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

        # TODO handle no Internet connection scenario
        weather = requests.get(url.format(city_name, OPENWEATHER_KEY)).json()

        if str(weather['cod']) == '404':
            return render(request, 'weather/index.html', {
                'error_message': 'City not found!'
            })
        elif str(weather['cod']) != '200':
            return render(request, 'weather/index.html', {
                'error_message': 'OpenWeather API error!'
            })
        else:
            new_city = City(name=weather['name'],
                            country_code=weather['sys']['country'],
                            openweather_id=weather['id'])
            new_city.save()
            return HttpResponseRedirect(reverse('weather:city_detail',
                                                args=(weather['name'], weather['id'])))
    else:
        city = city_set[0]
        print('In database: ' + city.name)
        return HttpResponseRedirect(reverse('weather:city_detail',
                                            args=(city.name, city.openweather_id)))


# 'city' is guaranteed to exist, but if it was deleted through admin panel or
# smth, the app will crash. And it also has to be deleted AFTER view_city post
# request, but BEFORE city_detail get request. So it's highly unlikely.
def city_detail(request, city_name, city_openweather_id):
    city = City.objects.filter(openweather_id=city_openweather_id)[0]
    current_weather_set = CurrentWeather.objects.filter(city=city)

    if not current_weather_set:
        current_weather = create_current_weather(city, city_openweather_id)
    else:
        current_weather = current_weather_set[0]

    if not current_weather.was_updated_last_minute():
        current_weather.update()

    return render(request, 'weather/city_detail.html', {'city': city, 'weather': current_weather})
