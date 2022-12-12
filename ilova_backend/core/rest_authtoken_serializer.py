from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import PhoneNumberAbstactUser

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        label=_("Phone number"),
        write_only = True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            try:
                username = PhoneNumberAbstactUser.objects.get(phone_number=phone_number).username
            except:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            user = authenticate(request=self.context.get('request'),
                                    username = username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone number" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
