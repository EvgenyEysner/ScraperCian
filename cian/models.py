from django.db import models
from django.contrib.auth.models import User
#  pip install django-currentuser
# https://pypi.org/project/django-currentuser/
from django_currentuser.middleware import get_current_authenticated_user
from PIL import Image as Img
from PIL import ImageDraw, ImageFont


class Apartment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', null=True)
    rooms = models.CharField('кол-во комнат', max_length=64, blank=True)
    price = models.CharField('цена', max_length=20, blank=True)
    address = models.CharField('Адрес', max_length=256, blank=True)
    desc = models.TextField('описание', blank=True)
    floor = models.CharField('этаж', max_length=10, blank=True)
    commission = models.CharField('коммисия', max_length=256, blank=True)

    def save(self, *args, **kwargs):  # переопределяю метод save  для получения текущего пользователя
        # Hack to pass the user to signal.
        self.owner = get_current_authenticated_user()
        super(Apartment, self).save(*args, **kwargs)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'квартира'
        verbose_name_plural = 'квартиры'


class Image(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    img = models.ImageField(upload_to='image/', blank=True)

    def save(self, *args, **kwargs):
        super().save()
        image = Img.open(self.img.path)
        cropped_image = image.crop((0, 0, 700, 650)) # лево, верх, право, низ
        # font = ImageFont.load_default()
        # font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 50)
        # pencil = ImageDraw.Draw(image)
        # pencil.point([(300, 300,), (650, 200)], fill=(0, 0, 0))
        # pencil.multiline_text((0, 830), 'Максим Пирогов \ +7-958-687-86-25 | +7-926-404-99-97', font=font, fill=(0, 0, 0))
        #   # Get dimensions

        # if width > 500 and height > 500:
        #     # keep ratio but shrink down
        #     image.thumbnail((width, height))
        #
        # # check which one is smaller
        # if height < width:
        #     # make square by cutting off equal amounts left and right
        #     left = (width - height) / 2
        #     right = (width + height) / 2
        #     top = 0
        #     bottom = height
        #     img = image.crop((left, top, right, bottom))
        #
        # elif width < height:
        #     # make square by cutting off bottom
        #     left = 0
        #     right = width
        #     top = 0
        #     bottom = width
        #     img = image.crop((left, top, right, bottom))
        #
        # if width > 300 and height > 300:
        #     image.thumbnail((300, 300))
        #
        cropped_image.save(self.img.path)

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'


class Url(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, related_name='urls', null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    url = models.URLField('ссылка')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'
        ordering = ['-created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('имя', max_length=120, blank=True)
    last_name = models.CharField('фамилия', max_length=240, blank=True)
    phone_1 = models.CharField('телефон 1', max_length=18, blank=True)
    phone_2 = models.CharField('телефон 2', max_length=18, blank=True)
    avatar = models.ImageField('аватар', default='avatars/avatar.png', upload_to='avatars/%Y/%m/%d')
    email = models.EmailField('email')

    def __str__(self):
        return "Профиль пользователя %s" % self.user

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
