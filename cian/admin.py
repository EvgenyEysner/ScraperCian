from django.contrib import admin
from django.utils.html import format_html  # для отображения фото в админке

from .models import Apartment, Image, Url


class InlineImage(admin.TabularInline):
    fk_name = 'apartment'
    model = Image
    readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.img.url}" style="width: 50px; height: 50px;"/>')
    image_tag.short_description = 'фото'


@admin.register(Apartment)
class AprtmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'rooms', 'price', 'desc', 'floor']
    inlines = [InlineImage, ]


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['created', 'url']

# admin.site.register(Image, ImageAdmin)


