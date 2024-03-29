from django.db import models
from django.utils import timezone

import datetime
import requests

import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")


class City(models.Model):
    name           = models.CharField(max_length=50)
    russian_name   = models.CharField(default="_",max_length=50)
    country_code   = models.CharField(max_length=3)
    openweather_id = models.IntegerField(default=0, unique=True)
    latitude       = models.FloatField(default=0)
    longitude      = models.FloatField(default=0)

    def __str__(self):
        # return self.name
        return self.russian_name

    class Meta:
        verbose_name_plural = 'Города'


class CurrentWeather(models.Model):
    # city        = models.ForeignKey(City, on_delete=models.CASCADE)
    city        = models.OneToOneField(City,
                                       on_delete=models.CASCADE,
                                       primary_key=True,
                                       related_name="weather")

    temp         = models.FloatField(default=0)
    feels_like   = models.FloatField(default=0)
    pressure     = models.IntegerField(default=0)
    humidity     = models.IntegerField(default=0)
    wind_speed   = models.FloatField(default=0)
    russian_desc = models.CharField('russian description',default="_", max_length=50)
    description  = models.CharField(max_length=50)
    desc_short   = models.CharField('short description', max_length=30)
    icon_name    = models.CharField(max_length=10)

    last_update = models.DateTimeField()

    def was_updated_last_minute(self):
        now = timezone.now()
        return now - datetime.timedelta(minutes=1) <= self.last_update <= now

    # TODO handle failed requests
    def update(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}'
        weather = requests.get(url.format(self.city.openweather_id, OPENWEATHER_KEY)).json()

        if str(weather['cod']) != '200':
            print("OpenWeather update failed!")
            return

        self.temp        = weather['main']['temp']
        self.feels_like  = weather['main']['feels_like']
        self.pressure    = weather['main']['pressure']
        self.humidity    = weather['main']['humidity']
        self.wind_speed  = weather['wind']['speed']
        self.description = weather['weather'][0]['description']
        self.desc_short  = weather['weather'][0]['main']
        self.icon_name   = weather['weather'][0]['icon']
        self.last_update = timezone.now()
        self.save()

    class Meta:
        verbose_name        = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        return self.city.name + ": " + self.desc_short


class CityStats(models.Model):
    city  = models.OneToOneField(City,
                                 on_delete=models.CASCADE,
                                 primary_key=True,
                                 related_name="stats")
    views = models.IntegerField(default=0)

    def inc_views(self):
        self.views += 1
        self.save()

    class Meta:
        verbose_name        = 'Статистика по городам'
        verbose_name_plural = 'Статистика по городам'

    def __str__(self):
        return self.city.name + ": " + str(self.views)


class StatsSummary(CityStats):
    class Meta:
        proxy = True
        verbose_name = "Дашборд"
        verbose_name_plural = "Дашборд"


def create_current_weather(city, city_openweather_id):
    # TODO handle failed requests
    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}'
    weather_json = requests.get(url.format(city_openweather_id, OPENWEATHER_KEY)).json()
    current_weather = CurrentWeather(
        city=city,
        temp=weather_json['main']['temp'],
        feels_like=weather_json['main']['feels_like'],
        pressure=weather_json['main']['pressure'],
        humidity=weather_json['main']['humidity'],
        wind_speed=weather_json['wind']['speed'],
        description=weather_json['weather'][0]['description'],
        desc_short=weather_json['weather'][0]['main'],
        icon_name=weather_json['weather'][0]['icon'],
        last_update=timezone.now()
    )
    current_weather.save()
    return current_weather
