from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def URLsNotAllowed(value):
    newValue = value.split()
    regex = URLValidator.regex
    for val in newValue:
        if not 'http://' in val or not 'https://' in val:
            prefix_val = 'http://' + val
            if regex.findall(prefix_val):
                raise ValidationError('Links are not allowed in messages.')
