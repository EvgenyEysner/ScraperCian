from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
import time
from django.core.files import File
from PIL import Image as Img
from django.shortcuts import render
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import urllib.request
from .models import Url, Apartment, Image

options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--incognito')
driver = webdriver.Firefox(executable_path='/home/evgeny/PycharmProjects/Cian/geckodriver', options=options)

header = Headers(
    # generate any browser & os headeers
    headers=False  # don`t generate misc headers
)

for i in range(10):
    headers = header.generate()


def crop_image(img):
    image = Img.open(img)
    im_crop = image.crop((300, 150, 900, 450))
    im_crop.save(f'{image}.jpg', quality=95)
    return image


def save_data(apartments_list):
    for ap in apartments_list:

        try:
            apartment = Apartment.objects.create(
                rooms=ap['rooms'],
                price=ap['price'],
                address=ap['address'],
                desc=ap['desc'],
                floor=ap['floor'],
            )
            for image in ap['photos']:
                im = Image()
                pic = urllib.request.urlretrieve(image)[0]
                crop_image(pic)
                im.img.save(image, File(open(pic, 'rb')))
                im.apartment_id = apartment.pk
                im.save()

        except Exception as e:
            print(e)
            break


def make_request(url):
    req = requests.get(url, headers=headers, timeout=3, stream=True)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup


@receiver(post_save, sender=Url)
def saved_url(instance, created, **kwargs):
    if created:
        url = instance.url
        soup = make_request(url)
        for link in soup.find_all('div', attrs={'data-name': 'LinkArea'}):
            url = link.find('a').get('href')
            driver.get(url)
            time.sleep(1)

            apartments = []
            try:
                rooms = driver.find_element(By.XPATH, '//div[1][@data-name="OfferTitle"]/h1').text
            except:
                rooms = None
            try:
                price = driver.find_element(By.XPATH, '//div[1]/div/span/span[1][@itemprop="price"]').text
            except:
                price = None
            try:
                address = driver.find_element(By.XPATH,
                                              '//section/div/div[1]/div[2]/span[@itemprop="name"]').get_attribute(
                    'content')
            except:
                address = None
            try:
                desc = driver.find_element(By.XPATH, '//div/span/p[@itemprop="description"]').text
            except:
                desc = None
            try:
                floor = driver.find_element(By.XPATH,
                                            '//div/div[4]/div[1][@data-testid="object-summary-description-value"]').text
            except:
                floor = None
            try:
                photos = [img.get_attribute('src') for img in driver.find_elements(By.CLASS_NAME, 'fotorama__img')]
            except:
                photos = None
            apartments.append(
                {
                    'rooms': rooms,
                    'price': price,
                    'address': address,
                    'desc': desc,
                    'floor': floor,
                    'photos': photos,
                }
            )
            save_data(apartments)



