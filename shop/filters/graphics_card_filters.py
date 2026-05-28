from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import GraphicsCard


class GraphicsCardChipManufacturerFilter(admin.SimpleListFilter):
    title = _("Chip Manufacturer")
    parameter_name = "chip_manufacturer"

    def lookups(self, request, model_admin):
        # از TextChoices مستقیماً استفاده می‌کنیم
        return GraphicsCard.ChipManufacturers.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chip_manufacturer=self.value())


class GraphicsCardInterfaceFilter(admin.SimpleListFilter):
    title = _("Interface")
    parameter_name = "interface"

    def lookups(self, request, model_admin):
        return GraphicsCard.Interfaces.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface=self.value())


class GraphicsCardVRAMTypeFilter(admin.SimpleListFilter):
    title = _("VRAM Type")
    parameter_name = "vram_type"

    def lookups(self, request, model_admin):
        return GraphicsCard.VRAMTypes.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(VRAM_type=self.value())


class GraphicsCardVRAMFilter(admin.SimpleListFilter):
    title = _("VRAM (GB)")
    parameter_name = "vram"

    LESS_THAN_4 = "lt_4"
    BETWEEN_4_AND_8 = "4_8"
    BETWEEN_8_AND_12 = "8_12"
    MORE_THAN_12 = "gt_12"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_4, _("Less than 4 GB")),
            (self.BETWEEN_4_AND_8, _("4 - 8 GB")),
            (self.BETWEEN_8_AND_12, _("8 - 12 GB")),
            (self.MORE_THAN_12, _("More than 12 GB")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_4:
            return queryset.filter(VRAM__lt=4)
        elif self.value() == self.BETWEEN_4_AND_8:
            return queryset.filter(VRAM__range=(4, 8))
        elif self.value() == self.BETWEEN_8_AND_12:
            return queryset.filter(VRAM__range=(8, 12))
        elif self.value() == self.MORE_THAN_12:
            return queryset.filter(VRAM__gt=12)


class GraphicsCardMinPowerSupplyFilter(admin.SimpleListFilter):
    title = _("Minimum PSU Required (W)")
    parameter_name = "min_power_supply"

    LESS_THAN_500 = "lt_500"
    BETWEEN_500_AND_750 = "500_750"
    BETWEEN_750_AND_1000 = "750_1000"
    MORE_THAN_1000 = "gt_1000"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_500, _("Less than 500W")),
            (self.BETWEEN_500_AND_750, _("500W - 750W")),
            (self.BETWEEN_750_AND_1000, _("750W - 1000W")),
            (self.MORE_THAN_1000, _("More than 1000W")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_500:
            return queryset.filter(min_power_supply_required__lt=500)
        elif self.value() == self.BETWEEN_500_AND_750:
            return queryset.filter(min_power_supply_required__range=(500, 750))
        elif self.value() == self.BETWEEN_750_AND_1000:
            return queryset.filter(min_power_supply_required__range=(750, 1000))
        elif self.value() == self.MORE_THAN_1000:
            return queryset.filter(min_power_supply_required__gt=1000)


class GraphicsCardFansCountFilter(admin.SimpleListFilter):
    title = _("Fans Count")
    parameter_name = "fans_count"

    ONE_FAN = "1"
    TWO_FANS = "2"
    THREE_FANS = "3"
    FOUR_FANS = "4+"  # برای 4 فن و بیشتر

    def lookups(self, request, model_admin):
        return (
            (self.ONE_FAN, _("1 Fan")),
            (self.TWO_FANS, _("2 Fans")),
            (self.THREE_FANS, _("3 Fans")),
            (self.FOUR_FANS, _("4+ Fans")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.ONE_FAN:
            return queryset.filter(fans_count=1)
        elif self.value() == self.TWO_FANS:
            return queryset.filter(fans_count=2)
        elif self.value() == self.THREE_FANS:
            return queryset.filter(fans_count=3)
        elif self.value() == self.FOUR_FANS:
            return queryset.filter(fans_count__gte=4)
