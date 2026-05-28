import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def national_code_validator(value):
    """
    Iranian national code validator function
    """
    # بررسی فرمت ۱۰ رقمی
    if not value.isdigit() or len(value) != 10:
        raise ValidationError(_("The national id must be 10 digits"))

    # محاسبه کد کنترل
    total = sum(int(value[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    check_digit = 0 if remainder < 2 else 11 - remainder

    # بررسی کد کنترل
    if int(value[9]) != check_digit:
        raise ValidationError(_("The national code is invalid"))


def postal_code_validator(value):
    """
    Validate Iranian postal code (10 digits + simple fraud prevention).
    """
    POSTAL_CODE_REGEX = re.compile(r"^(?!0{10})(?!1{10})[13-9]\d{9}$")
    if not POSTAL_CODE_REGEX.match(value):
        raise ValidationError(_("Invalid Iranian postal code."))
