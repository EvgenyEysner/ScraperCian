from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from fake_useragent import UserAgent
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.request
from .models import Url, Apartment, Image, Profile
import json
import time
import random


start_json_template = "window._cianConfig['frontend-offer-card'] = "

ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

proxy = {

     'https': 'http://186.65.114.25:9898',
     'http': 'http://186.65.114.25:9898'
}


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email = instance.email
        )


def save_data(apartments_list):  # save the scraped data to the database
    for ap in apartments_list:
        try:
            apartment = Apartment.objects.create(
                rooms=ap['rooms'],
                price=ap['price'],
                address=ap['address'],
                desc=ap['desc'],
                floor=ap['floor'],
                commission=ap['commission'],
            )
            for image in ap['photos']:
                im = Image()
                pic = urllib.request.urlretrieve(image)[0] # download images
                im.img.save(image, File(open(pic, 'rb'))) # save images to media directory
                im.apartment_id = apartment.pk
                im.save()

        except Exception as e:
            print(e)
            break


@receiver(post_save, sender=Url)
def saved_url(instance, created, **kwargs):
    if created:
        url = instance.url

        s = requests.Session()

        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)

        response = s.get(url, headers=headers, proxies=proxy, timeout=random.randint(1, 5)) # proxies={'http': 'http://138.59.206.183:9915'}
        html = response.text
        # time.sleep(random.randint(1, 4))
        if start_json_template in html: # get json from website
            start = html.index(start_json_template) + len(start_json_template)
            end = html.index('</script>', start)
            json_raw = html[start:end].strip()[:-1]
            js = json.loads(json_raw)
            time.sleep(random.randint(1, 5))

            for item in js:
                apartments = []

                if item['key'] == 'defaultState':
                    try:
                        price = item['value']['offerData']['offer']['bargainTerms']['price']
                    except:
                        price = None
                    try:
                        floor = item['value']['offerData']['offer']['floorNumber']
                    except:
                        floor = None
                    try:
                        desc = item['value']['offerData']['offer']['description']
                    except:
                        desc = None
                    try:
                        region = item['value']['offerData']['offer']['geo']['address'][0]['fullName']
                    except:
                        region = None
                    try:
                        town = item['value']['offerData']['offer']['geo']['address'][1]['fullName']
                    except:
                        town = None
                    try:
                        street = item['value']['offerData']['offer']['geo']['address'][-2]['fullName']
                    except:
                        street = None
                    try:
                        house_number = item['value']['offerData']['offer']['geo']['address'][-1]['fullName']
                    except:
                        house_number = None
                    try:
                        address = region + ', ' + town + ', ' + street + ' ' + house_number
                        # address = item['value']['offerData']['offer']['geo']['address']
                    except:
                        address = None
                    try:
                        rooms = item['value']['offerData']['offer']['roomsCount']
                    except:
                        rooms = None
                    try:
                        commission = item['value']['offerData']['offer']['bargainTerms']['agentFee']
                    except:
                        commission = None
                    try:
                        photos = []

                        for photo in item['value']['offerData']['offer']['photos']:
                            photos.append(photo['fullUrl'])
                    except:
                        photos = None
                    time.sleep(random.randint(1,3))
                    apartments.append(
                        {
                            'rooms': rooms,
                            'price': price,
                            'address': address,
                            'desc': desc,
                            'floor': floor,
                            'photos': photos,
                            'commission': commission,
                        }
                    )
                    save_data(apartments)
                    instance.delete()


