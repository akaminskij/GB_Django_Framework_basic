import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


NULLABLE = {'blank': True, 'null': True}


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)  # default=(now() + timedelta(hours=48))

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expired + timedelta(hours=48):
            return False
        return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    UNKNOWN = 'U'

    GENDER = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (UNKNOWN, 'Н'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, **NULLABLE)
    about_Me = models.TextField(verbose_name='о себе', max_length=512, **NULLABLE)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER, blank=True, default=UNKNOWN)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()


