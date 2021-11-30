from django.forms import ModelForm, URLInput
from .models import Url


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