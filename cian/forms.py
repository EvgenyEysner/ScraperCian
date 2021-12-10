from django.forms import ModelForm, URLInput, HiddenInput, FloatField, FileInput
from .models import Url, Apartment, Image
from PIL import Image as Img


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


class ImageForm(ModelForm):
    x = FloatField(widget=HiddenInput())
    y = FloatField(widget=HiddenInput())
    width = FloatField(widget=HiddenInput())
    height = FloatField(widget=HiddenInput())

    class Meta:
        model = Image
        fields = ('img', 'x', 'y', 'width', 'height', )

        widgets = {
            FileInput(attrs={
                'class': 'form-control',
            }),
        }

    def save(self):
        photo = super(ImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Img.open(photo.img)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400), Img.ANTIALIAS)
        resized_image.save(photo.img.path)

        return resized_image