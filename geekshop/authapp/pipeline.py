from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    base_url = 'https://api.vk.com/method/users.get/'

    fields_for_requests = ['bdate', 'sex', 'about', 'photo_max_orig']

    params = {
        'fields': ','.join(fields_for_requests),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)

    # print(api_response)

    if api_response.status_code != 200:
        return

    api_data = api_response.json()['response'][0]

    if 'sex' in api_data:
        if api_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif api_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.UNKNOWN

    if 'about' in api_data:
        user.shopuserprofile.about_Me = api_data['about']

    if 'bdate' in api_data:
        bdate = datetime.strptime(api_data['bdate'], "%d.%m.%Y").date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'photo_max_orig' in api_data:
        # print(api_data['photo_max_orig'])
        avatar_url = api_data['photo_max_orig']
        avatar_response = requests.get(avatar_url)
        avatar_path = f'{settings.MEDIA_ROOT}/users/{user.pk}.jpg'
        with open(avatar_path, 'wb') as avatar_file:
            avatar_file.write(avatar_response.content)

    user.avatar = f'users/{user.pk}.jpg'


    user.save()

    # api_url = urlunparse(('https',
    #                       'api.vk.com',
    #                       '/method/users.get',
    #                       None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                                             access_token=response['access_token'],
    #                                             v='5.92')),
    #                       None
    #                       ))
    #
    # resp = requests.get(api_url)
    # if resp.status_code != 200:
    #     return
    #
    # data = resp.json()['response'][0]
    # if data['sex']:
    #     user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE
    #
    # if data['about']:
    #     user.shopuserprofile.aboutMe = data['about']
    #
    # if data['bdate']:
    #     bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    #
    #     age = timezone.now().date().year - bdate.year
    #     if age < 18:
    #         user.delete()
    #         raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    #
    # user.save()
