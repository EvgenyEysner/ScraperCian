from django.forms import ModelForm, URLInput
from .models import Url, Apartment


class UrlForm(ModelForm):
    class Meta:
        model = Url
        fields = ['url']

        widgets = {
            'url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'ссылка...',
            }),
        }

class ApartmentEditForm(ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'