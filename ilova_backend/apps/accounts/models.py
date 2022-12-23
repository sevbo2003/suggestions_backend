from __future__ import unicode_literals

import datetime
import hashlib
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers.phone_number_user_manager import PhoneNumberUserManager
from apps.notification.models import Mahalla
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from eskiz_sms import EskizSMS


eskiz = EskizSMS(
            email=getattr(settings, 'ESKIZ_EMAIL', None),
            password=getattr(settings, 'ESKIZ_PASSWORD', None),
        )
class Tuman(models.Model):
    tuman = models.CharField(max_length=200)
    mahallalar = models.ManyToManyField(Mahalla)

    def __str__(self) -> str:
        return self.tuman


class Viloyat(models.Model):
    viloyat = models.CharField(max_length=200)
    tumanlar = models.ManyToManyField(Tuman)
    

class PhoneNumberAbstactUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    objects = PhoneNumberUserManager()
    REQUIRED_FIELDS = ['email', 'phone_number']
    mahallalar = models.ManyToManyField(Mahalla, related_name='users',null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone_number.as_e164


class PhoneToken(models.Model):
    phone_number = PhoneNumberField(editable=False)
    otp = models.CharField(max_length=40, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP Token"
        verbose_name_plural = "OTP Tokens"

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.otp)

    @classmethod
    def create_otp_for_number(cls, number):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        otps = cls.objects.filter(phone_number=number, timestamp__range=(today_min, today_max))
        if otps.count() <= getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10):
            otp = cls.generate_otp(length=getattr(settings, 'PHONE_LOGIN_OTP_LENGTH', 6))
            phone_token = PhoneToken(phone_number=number, otp=otp)
            phone_token.save()
            message = f"Sizning bir martalik parolingiz: {otp}"
            # eskiz.send_sms(str(number)[1:], message, from_whom='4546')
            return phone_token
        else:
            return False

    @classmethod
    def generate_otp(cls, length=6):
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp