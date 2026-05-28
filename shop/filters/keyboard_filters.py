from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import Keyboard


class KeyboardConnectionTypeFilter(admin.SimpleListFilter):
    title = _("Connection Type")
    parameter_name = "connection_type"

    def lookups(self, request, model_admin):
        return Keyboard.ConnectionType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(connection_type=self.value())


class KeyboardSwitchTypeFilter(admin.SimpleListFilter):
    title = _("Switch Type")
    parameter_name = "switch_type"

    def lookups(self, request, model_admin):
        return Keyboard.SwitchType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(switch_type=self.value())


class KeyboardLayoutFilter(admin.SimpleListFilter):
    title = _("Layout")
    parameter_name = "layout"

    def lookups(self, request, model_admin):
        return Keyboard.KeyboardLayout.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(layout=self.value())


class HasNumericPadFilter(admin.SimpleListFilter):
    title = _("Numeric Pad")
    parameter_name = "has_numeric_pad"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(has_numeric_pad=True)
        elif self.value() == "no":
            return queryset.filter(has_numeric_pad=False)


class KeyboardBacklightFilter(admin.SimpleListFilter):
    title = _("Backlight Type")
    parameter_name = "backlight"

    def lookups(self, request, model_admin):
        return Keyboard.BacklightType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(backlight=self.value())


class KeyboardIsMechanicalFilter(admin.SimpleListFilter):
    title = _("Mechanical Keyboard")
    parameter_name = "is_mechanical"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(is_mechanical=True)
        elif self.value() == "no":
            return queryset.filter(is_mechanical=False)


class KeyboardKeyCountFilter(admin.SimpleListFilter):
    title = _("Key Count")
    parameter_name = "key_count"

    # Define common key count ranges (adjust as needed based on your data)
    UP_TO_87 = "upto_87"  # Tenkeyless
    UP_TO_104 = "upto_104"  # Standard full size
    MORE_THAN_104 = "gt_104"  # Extended or custom layouts
    NOT_SPECIFIED = "not_specified"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_87, _("Up to 87 Keys (e.g., Tenkeyless)")),
            (self.UP_TO_104, _("Up to 104 Keys (e.g., Full Size)")),
            (self.MORE_THAN_104, _("More than 104 Keys")),
            (self.NOT_SPECIFIED, _("Not Specified")),
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.UP_TO_87:
                return queryset.filter(key_count__lte=87)
            elif self.value() == self.UP_TO_104:
                return queryset.filter(key_count__lte=104)
            elif self.value() == self.MORE_THAN_104:
                return queryset.filter(key_count__gt=104)
            elif self.value() == self.NOT_SPECIFIED:
                return queryset.filter(key_count__isnull=True)


class KeyboardInterfaceFilter(admin.SimpleListFilter):
    title = _("Interface")
    parameter_name = "interface"

    def lookups(self, request, model_admin):
        # You can predefine common interfaces or dynamically fetch distinct values
        return (
            ("usb", _("USB")),
            ("bluetooth", _("Bluetooth")),
            ("2.4ghz", _("2.4GHz Wireless")),
            ("usb-c", _("USB-C")),
            ("thunderbolt", _("Thunderbolt")),  # Though less common for keyboards
        )

    def queryset(self, request, queryset):
        if self.value():
            # Case-insensitive search for the interface
            return queryset.filter(interface__icontains=self.value())


class KeyboardBatteryLifeFilter(admin.SimpleListFilter):
    title = _("Battery Life (Hours)")
    parameter_name = "battery_life_hours"

    # Define common battery life ranges (adjust as needed)
    UP_TO_20 = "upto_20"
    UP_TO_50 = "upto_50"
    UP_TO_100 = "upto_100"
    MORE_THAN_100 = "gt_100"
    NOT_SPECIFIED = "not_specified"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_20, _("Up to 20 Hours")),
            (self.UP_TO_50, _("Up to 50 Hours")),
            (self.UP_TO_100, _("Up to 100 Hours")),
            (self.MORE_THAN_100, _("More than 100 Hours")),
            (self.NOT_SPECIFIED, _("Not Specified")),
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.UP_TO_20:
                return queryset.filter(battery_life_hours__lte=20)
            elif self.value() == self.UP_TO_50:
                return queryset.filter(battery_life_hours__lte=50)
            elif self.value() == self.UP_TO_100:
                return queryset.filter(battery_life_hours__lte=100)
            elif self.value() == self.MORE_THAN_100:
                return queryset.filter(battery_life_hours__gt=100)
            elif self.value() == self.NOT_SPECIFIED:
                return queryset.filter(battery_life_hours__isnull=True)


class KeyboardWaterproofFilter(admin.SimpleListFilter):
    title = _("Waterproof")
    parameter_name = "waterproof"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(waterproof=True)
        elif self.value() == "no":
            return queryset.filter(waterproof=False)
