from django.urls import path

from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:city_name>-<int:city_openweather_id>/', views.city_detail, name='city_detail'),
    path('view_city/', views.view_city, name='view_city'),
]
