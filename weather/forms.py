from django.forms import ModelForm, TextInput
from .models import City


class ShowCityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'City name'}),
        }
