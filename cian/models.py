from django.db import models


class Profile(models.Model):
    pass


class Apartment(models.Model):
    rooms = models.CharField('кол-во комнат', max_length=64, null=True)
    price = models.CharField('цена', max_length=20, null=True, blank=True)
    address = models.CharField('Адрес', max_length=256, null=True, blank=True)
    desc = models.TextField('описание', null=True, blank=True)
    floor = models.CharField('этаж', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'квартира'
        verbose_name_plural = 'квартиры'


class Image(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    img = models.ImageField(upload_to='image/', null=True, blank=True)

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'


class Url(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    url = models.URLField('ссылка')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'
        ordering = ['-created']
