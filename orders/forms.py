from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .models import Order


class OrderForm(forms.ModelForm):
    change_name = forms.BooleanField(
        label=_("Also change first_name and last_name of my account."), required=False
    )

    phone_number = PhoneNumberField(
        label=_("Phone number"),
        region="IR",
        help_text=_(
            "If you have disabled advertising messages, SMS won't be sent to your number."
        ),
        error_messages={
            "required": _("Enter phone number."),
            "invalid": _("Enter a valid phone number."),
        },
    )

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "order_notes",
        ]

        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "address": _("Address"),
            "order_notes": _("Order notes"),
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": _("First name")}),
            "last_name": forms.TextInput(attrs={"placeholder": _("Last name")}),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": _("Enter your address")}
            ),
            "order_notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": _("Additional notes for your order (optional)"),
                }
            ),
        }
