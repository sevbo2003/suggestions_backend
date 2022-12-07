import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable
from core.validators import validate_number


class UserTypes(models.TextChoices):
    ADMIN = "AD", "ADMIN"
    USER = "US", "USER"


class CustomUser(AbstractUser):
    username = PhoneNumberField(unique=True, validators=[validate_number])
    user_type = models.CharField(max_length=2, choices=UserTypes.choices, default=UserTypes.USER)
    email = models.EmailField(null=True, blank=True)
    first_name = None
    last_name = None
    security_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        try:
            return self.username.as_e164
        except:
            return self.username

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        code = get_random_string(token_length, allowed_chars="0123456789")
        return code

    def is_security_code_expired(self):
        expiration_date = self.sent() + datetime.timedelta(
            minutes=settings.TOKEN_EXPIRE_MINUTES
        )
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        self.security_code = self.generate_security_code()
        self.sent = timezone.now

        print(f'Sending security code {self.security_code} to phone {self.username}')
        

    def check_verification(self, security_code):
        if (
            not self.is_security_code_expired() and
            security_code == self.security_code and
            self.is_verified == False
        ):
            self.is_verified = True
            self.save()
        else:
            raise NotAcceptable(
                _("Your security code is wrong, expired or this phone is verified before."))

        return self.is_verified
