from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BluetoothDongleMaxRangeFilter(admin.SimpleListFilter):
    title = _("Max Range (Meters)")
    parameter_name = "max_range"

    # Define common range buckets
    UP_TO_5M = "upto_5"
    UP_TO_10M = "upto_10"
    UP_TO_20M = "upto_20"
    MORE_THAN_20M = "gt_20"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_5M, _("Up to 5 Meters")),
            (self.UP_TO_10M, _("Up to 10 Meters")),
            (self.UP_TO_20M, _("Up to 20 Meters")),
            (self.MORE_THAN_20M, _("More than 20 Meters")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_5M:
            return queryset.filter(max_range__lte=5)
        elif self.value() == self.UP_TO_10M:
            return queryset.filter(max_range__lte=10)
        elif self.value() == self.UP_TO_20M:
            return queryset.filter(max_range__lte=20)
        elif self.value() == self.MORE_THAN_20M:
            return queryset.filter(max_range__gt=20)


class BluetoothDongleInterfaceTypeFilter(admin.SimpleListFilter):
    title = _("Interface Type")
    parameter_name = "interface_type"

    def lookups(self, request, model_admin):
        # Define common interface types
        return (
            ("USB-A", _("USB-A")),
            ("USB-C", _("USB-C")),
            ("Internal", _("Internal")),  # For PCIe cards, etc.
            ("Proprietary", _("Proprietary")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface_type__iexact=self.value())


class BluetoothDongleBluetoothVersionFilter(admin.SimpleListFilter):
    title = _("Bluetooth Version")
    parameter_name = "bluetooth_version"

    # Define common version buckets
    VERSION_5_3 = "5.3"
    VERSION_5_2 = "5.2"
    VERSION_5_1 = "5.1"
    VERSION_5_0 = "5.0"
    VERSION_4_2 = "4.2"
    VERSION_4_0 = "4.0"

    def lookups(self, request, model_admin):
        return (
            (self.VERSION_5_3, _("5.3")),
            (self.VERSION_5_2, _("5.2")),
            (self.VERSION_5_1, _("5.1")),
            (self.VERSION_5_0, _("5.0")),
            (self.VERSION_4_2, _("4.2")),
            (self.VERSION_4_0, _("4.0")),
            # Add more as needed, or consider a range filter for broader searches
        )

    def queryset(self, request, queryset):
        if self.value():
            # Use Decimal for exact comparison if possible, or __startswith for broader matches
            return queryset.filter(bluetooth_version=self.value())
