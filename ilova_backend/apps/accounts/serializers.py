from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from core.validators import validate_number
from .exceptions import (
    AccountNotRegisteredException,
    InvalidCredentialsException,
    AccountDisabledException,
)
import pyotp

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    username = PhoneNumberField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_('A user with this phone number already exists.')
            ),
            validate_number,
        ],
    )

    class Meta:
        model = User
        fields = ('username', )
        
    def get_cleaned_data_extra(self):
        return {
            'phone_number': self.validated_data.get('username', ''),
        }
    
# class SmsSerializers(serializers.Serializer):
#     sms_code = serializers.CharField(max_length=6, required=True)
#     phone_number = PhoneNumberField(required=True)
    
#     def validate(self, data):
#         user = data.get('phone_number', None)
#         if validate_number(user):
#             if User.objects.get(username=user):
#                 user = User.objects.get(username=user)
        
#         # if not user.is_active:
#         #     raise AccountDisabledException()
#         # time_otp = pyotp.TOTP(user.key, interval=300)
#         # if not time_otp.verify(data['sms_code']):
#         #     raise InvalidCredentialsException()
#         # return data

