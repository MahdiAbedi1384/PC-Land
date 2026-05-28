from django import forms
from django.utils.translation import gettext_lazy as _


class AddToCartProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        error_messages={
            "required": _("Enter number of product!"),
            "min_value": _("Number of products can't be negative or zero!"),
            "max_value": _("Number of products can't be more than 30."),
            "invalid": _("Please enter a valid integer number."),
        },
        widget=forms.NumberInput(
            attrs={"class": "quantity-input", "style": "width:50px;text-align:center;"}
        ),
    )

    # برای تشخیص رفتار add یا replace
    replace = forms.BooleanField(required=False, widget=forms.HiddenInput)

    def clean_quantity(self):
        q = self.cleaned_data["quantity"]

        # نمونه‌ای از کنترل خاص:
        if q > 100:
            raise forms.ValidationError(
                _(
                    "You cannot order exactly 7 items! if you have more than 100 items contact to support!"
                )
            )

        return q
