# Generated by Django 4.0.5 on 2022-07-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_alter_city_openweather_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='openweather_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
