from django import template
from django.conf import settings

register = template.Library()


def media_for_products(image):
    if not image:
        image = 'products_images/default.png'

    # if not file_exists(f'{settings.MEDIA_ROOT}{image}'):
    #     image = 'products_images/default.png'

    return f'{settings.MEDIA_URL}{image}'


@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        avatar = 'users/default-user-image1.png'

    return f'{settings.MEDIA_URL}{avatar}'


register.filter('media_for_products', media_for_products)
