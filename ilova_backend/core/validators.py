import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_number(number):
    if not re.match(r'^\+998\d{9}$', number):
        raise ValidationError(
            _('%(value)s is not a valid number'),
            params={'value': number},
        )
    
    