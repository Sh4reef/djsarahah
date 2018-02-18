import re

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def custom_username_validator(value):
    regex = re.compile(r'[\W+]')
    if regex.findall(value) or '_' in value:
        raise ValidationError('Username must contains only, Numbers, Letters')

def custom_username_validator_updated(value):
    newreg = re.compile(r'[a-zA-Z0-9]')
    sub_value = newreg.sub('', value)
    if sub_value.__len__() != 0:
        raise ValidationError('Username must contains only, Numbers, English letters')

custom_validators = [custom_username_validator_updated]
