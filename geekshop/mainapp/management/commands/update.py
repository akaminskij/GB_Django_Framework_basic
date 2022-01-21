import json
from django.conf import settings
from django.core.management import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            # if not user.shopuserprofile:
            ShopUserProfile.objects.create(user=user)


