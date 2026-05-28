from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import InternalHDD


# --- InternalHDDBrand Filter ---
class InternalHDDBrandFilter(admin.SimpleListFilter):
    title = _("Brand")
    parameter_name = "brand"

    # ✅ لیست ثابت برندهای رایج (تنها برای نمونه — بسته به دیتابیس واقعی تنظیم شود)
    BRAND_CHOICES = [
        ("Seagate", _("Seagate")),
        ("Western Digital", _("Western Digital")),
        ("Toshiba", _("Toshiba")),
        ("Samsung", _("Samsung")),
        ("Hitachi", _("Hitachi")),
        ("other", _("Other")),
    ]

    def lookups(self, request, model_admin):
        # بدون هیچ کوئری دیتابیس
        return self.BRAND_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == "other":
            # فیلتر کردن برندهایی که در لیست ثابت نیستند
            known_brands = [b[0] for b in self.BRAND_CHOICES if b[0] != "other"]
            return queryset.exclude(brand__in=known_brands)

        # فیلتر کردن برند انتخاب‌شده
        return queryset.filter(brand__icontains=value)


# --- InternalHDDCapacity Filter (in TB) ---
class InternalHDDCapacityFilter(admin.SimpleListFilter):
    title = _("capacity (TB)")
    parameter_name = "capacity_tb"

    def lookups(self, request, model_admin):
        # Using common TB capacities. You might want to dynamically fetch these
        # or define a wider range if needed.
        return [
            ("1.0", _("1 TB")),
            ("2.0", _("2 TB")),
            ("4.0", _("4 TB")),
            ("8.0", _("8 TB")),
            ("16.0", _("16 TB")),
            ("18.0", _("18 TB")),  # Common for high capacity drives
            ("20.0", _("20 TB")),
            ("22.0", _("22 TB")),  # Common for high capacity drives
            ("24.0", _("24 TB")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            # Ensure comparison is done with Decimal
            return queryset.filter(capacity_tb=Decimal(self.value()))
        return queryset


# --- InternalHDDInterface Filter ---
class InternalHDDInterfaceFilter(admin.SimpleListFilter):
    title = _("interface")
    parameter_name = "interface"

    def lookups(self, request, model_admin):
        # Using choices directly from the model's field
        # Assuming 'interface_choices' is defined or accessible like this:
        try:
            # Try accessing choices directly from the field if it's a CharField with choices
            return InternalHDD.interface.field.choices
        except AttributeError:
            # Fallback if choices are defined differently
            return getattr(InternalHDD, "interface_choices", [])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface=self.value())
        return queryset


# --- InternalHDDFormFactor Filter ---
class InternalHDDFormFactorFilter(admin.SimpleListFilter):
    title = _("form factor")
    parameter_name = "form_factor"

    def lookups(self, request, model_admin):
        try:
            return InternalHDD.form_factor.field.choices
        except AttributeError:
            return getattr(InternalHDD, "form_factor_choices", [])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(form_factor=self.value())
        return queryset


# --- InternalHDDRPM Filter ---
class InternalHDDRPMFilter(admin.SimpleListFilter):
    title = _("RPM")
    parameter_name = "rpm"

    def lookups(self, request, model_admin):
        try:
            return InternalHDD.rpm.field.choices
        except AttributeError:
            return getattr(InternalHDD, "rpm_choices", [])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rpm=self.value())
        return queryset


# --- InternalHDDCache Filter ---
class InternalHDDCacheFilter(admin.SimpleListFilter):
    title = _("Cache (MB)")
    parameter_name = "cache_mb"

    def lookups(self, request, model_admin):
        # Using common cache sizes. Adjust as needed.
        return [
            ("64", _("64 MB")),
            ("128", _("128 MB")),
            ("256", _("256 MB")),
            ("512", _("512 MB")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cache_mb=int(self.value()))
        return queryset


# --- InternalHDDISExternal Filter ---
class InternalHDDISExternalFilter(admin.SimpleListFilter):
    title = _("Is External")
    parameter_name = "is_external"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(is_external=(self.value() == "True"))
        return queryset


# --- InternalHDDPowerConsumption Filter ---
class InternalHDDPowerConsumptionFilter(admin.SimpleListFilter):
    title = _("Power Consumption (Watts)")
    parameter_name = "power_consumption_watts"

    def lookups(self, request, model_admin):
        # Using common power consumption values. Adjust as needed.
        return [
            ("5.0", _("5.0W")),
            ("7.5", _("7.5W")),
            ("10.0", _("10.0W")),
            ("12.5", _("12.5W")),
            ("15.0", _("15.0W")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(power_consumption_watts=Decimal(self.value()))
        return queryset


# --- InternalHDDOperatingTemperature Filter ---
class InternalHDDOperatingTemperatureFilter(admin.SimpleListFilter):
    title = _("Operating Temperature")
    parameter_name = "operating_temperature_celsius"

    def lookups(self, request, model_admin):
        # Providing common temperature ranges.
        return [
            ("0-60", _("0°C to 60°C")),
            ("5-45", _("5°C to 45°C")),
            ("10-50", _("10°C to 50°C")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            # This filter assumes a specific format in lookups and will need
            # more complex logic if the actual data varies widely.
            # For now, we'll filter based on the exact string in the lookup.
            # A more robust solution might involve parsing the range.
            return queryset.filter(
                operating_temperature_celsius__icontains=self.value()
            )
        return queryset
