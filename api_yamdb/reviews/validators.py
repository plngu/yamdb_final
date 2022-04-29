import datetime
from django.core.exceptions import ValidationError


def validate_year(year):
    if year > datetime.datetime.now().year:
        raise ValidationError(
            'Select past or current year.The future is yet to come.'
        )
