from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from iranian_cities.models import City, Province
from phonenumber_field.modelfields import PhoneNumberField

from .validators import national_code_validator, postal_code_validator


class CustomUser(AbstractUser):
    GENDER_CHOICES_Male = "M"
    GENDER_CHOICES_Female = "F"
    GENDER_CHOICES = (
        (GENDER_CHOICES_Male, "Male"),
        (GENDER_CHOICES_Female, "Female"),
    )
    nat_code = models.CharField(
        _("National Code"),
        max_length=10,
        unique=True,
        validators=[national_code_validator],
        null=True,
        blank=True,
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    phone_number = PhoneNumberField(
        region=settings.PHONENUMBER_DEFAULT_REGION,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    phone_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Addresses(models.Model):
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    full_name = models.CharField(
        verbose_name=_("Full Name"), max_length=255, null=True, blank=True
    )
    phone_number = PhoneNumberField(
        region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True
    )
    province = models.ForeignKey(
        verbose_name=_("Province"), to=Province, on_delete=models.SET_NULL, null=True
    )
    city = models.ForeignKey(
        verbose_name=_("City"), to=City, on_delete=models.SET_NULL, null=True
    )
    full_address = models.TextField(verbose_name=_("Full Address"), max_length=500)
    postal_code = models.CharField(
        verbose_name=_("Postal Code"),
        null=True,
        blank=True,
        max_length=10,
        validators=[postal_code_validator],
    )
    is_default = models.BooleanField(verbose_name=_("Is Default"), default=False)

    def set_full_name(self):
        if not self.full_name:
            self.full_name = f"{self.user.first_name} {self.user.last_name}"

    def set_phone_number(self):
        if not self.phone_number:
            # اول از خود کاربر
            if self.user.phone_number:
                self.phone_number = self.user.phone_number
            # بعد از PhoneNumber مرتبط (otp_phone_number)
            elif hasattr(self.user, "otp_phone_number") and self.user.otp_phone_number:
                self.phone_number = self.user.otp_phone_number.phone_number

    def save(self, *args, **kwargs):
        """فراخوانی توابع قبل از ذخیره‌سازی"""
        self.set_full_name()
        self.set_phone_number()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
