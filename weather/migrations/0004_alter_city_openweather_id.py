# Generated by Django 4.0.5 on 2022-07-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_remove_city_last_update_city_country_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='openweather_id',
            field=models.IntegerField(default=0),
        ),
    ]
