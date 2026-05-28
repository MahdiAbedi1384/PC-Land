from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CaseSizeFilter(admin.SimpleListFilter):
    title = _("Case Size")
    parameter_name = "case_size"

    # Define common case sizes or ranges
    FULL_TOWER = "full_tower"
    MID_TOWER = "mid_tower"
    MINI_TOWER = "mini_tower"
    SMALL_FORM_FACTOR = "sff"  # Small Form Factor

    def lookups(self, request, model_admin):
        return (
            (self.FULL_TOWER, _("Full Tower")),
            (self.MID_TOWER, _("Mid Tower")),
            (self.MINI_TOWER, _("Mini Tower")),
            (self.SMALL_FORM_FACTOR, _("Small Form Factor (SFF)")),
            # Add more specific sizes if needed, e.g., "Cube Case"
        )

    def queryset(self, request, queryset):
        if self.value() == self.FULL_TOWER:
            # Adjust query based on your actual size naming convention
            return queryset.filter(size__icontains="full tower")
        elif self.value() == self.MID_TOWER:
            return queryset.filter(size__icontains="mid tower")
        elif self.value() == self.MINI_TOWER:
            return queryset.filter(size__icontains="mini tower")
        elif self.value() == self.SMALL_FORM_FACTOR:
            return queryset.filter(size__icontains="sff")  # or other SFF terms


class CaseFormFactorFilter(admin.SimpleListFilter):
    title = _("Case Form Factor")
    parameter_name = "case_form_factor"

    # Example values, adjust based on your data
    ATX = "atx"
    MICRO_ATX = "micro_atx"
    MINI_ITX = "mini_itx"

    def lookups(self, request, model_admin):
        return (
            (self.ATX, _("ATX")),
            (self.MICRO_ATX, _("Micro-ATX")),
            (self.MINI_ITX, _("Mini-ITX")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(case_form_factor__icontains=self.value())


class MaxCPUCoolerHeightFilter(admin.SimpleListFilter):
    title = _("Max CPU Cooler Height (mm)")
    parameter_name = "max_cpu_cooler_height"

    LESS_THAN_100 = "lt_100"
    BETWEEN_100_AND_160 = "100_160"
    MORE_THAN_160 = "gt_160"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_100, _("Less than 100mm")),
            (self.BETWEEN_100_AND_160, _("100mm - 160mm")),
            (self.MORE_THAN_160, _("More than 160mm")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_100:
            return queryset.filter(max_cpu_cooler_height__lt=100)
        elif self.value() == self.BETWEEN_100_AND_160:
            return queryset.filter(max_cpu_cooler_height__range=(100, 160))
        elif self.value() == self.MORE_THAN_160:
            return queryset.filter(max_cpu_cooler_height__gt=160)


class MaxGPUCardLengthFilter(admin.SimpleListFilter):
    title = _("Max GPU Length (mm)")
    parameter_name = "max_gpu_length"

    LESS_THAN_280 = "lt_280"
    BETWEEN_280_AND_330 = "280_330"
    MORE_THAN_330 = "gt_330"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_280, _("Less than 280mm")),
            (self.BETWEEN_280_AND_330, _("280mm - 330mm")),
            (self.MORE_THAN_330, _("More than 330mm")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_280:
            return queryset.filter(max_graphics_card_length__lt=280)
        elif self.value() == self.BETWEEN_280_AND_330:
            return queryset.filter(max_graphics_card_length__range=(280, 330))
        elif self.value() == self.MORE_THAN_330:
            return queryset.filter(max_graphics_card_length__gt=330)


class CaseMaterialFilter(admin.SimpleListFilter):
    title = _("Case Material")
    parameter_name = "case_material"

    # Example materials
    STEEL = "steel"
    ALUMINUM = "aluminum"
    TEMPERED_GLASS = "tempered_glass"
    PLASTIC = "plastic"

    def lookups(self, request, model_admin):
        return (
            (self.STEEL, _("Steel")),
            (self.ALUMINUM, _("Aluminum")),
            (self.TEMPERED_GLASS, _("Tempered Glass")),
            (self.PLASTIC, _("Plastic")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(case_material__icontains=self.value())


class CaseDriveBayFilter(admin.SimpleListFilter):
    title = _("Drive Bays")
    parameter_name = "drive_bays"

    # Filters for 3.5 inch bays, can be extended for 2.5 or combined
    ZERO_OR_MORE_3_5 = "0_plus_3_5"
    TWO_OR_MORE_3_5 = "2_plus_3_5"
    FOUR_OR_MORE_3_5 = "4_plus_3_5"

    def lookups(self, request, model_admin):
        return (
            (self.ZERO_OR_MORE_3_5, _('0+ 3.5" Bays')),
            (self.TWO_OR_MORE_3_5, _('2+ 3.5" Bays')),
            (self.FOUR_OR_MORE_3_5, _('4+ 3.5" Bays')),
        )

    def queryset(self, request, queryset):
        if self.value() == self.ZERO_OR_MORE_3_5:
            return queryset.filter(Number_of_3_p_5_inch_drive_bays__gte=0)
        elif self.value() == self.TWO_OR_MORE_3_5:
            return queryset.filter(Number_of_3_p_5_inch_drive_bays__gte=2)
        elif self.value() == self.FOUR_OR_MORE_3_5:
            return queryset.filter(Number_of_3_p_5_inch_drive_bays__gte=4)


class CaseExpansionSlotsFilter(admin.SimpleListFilter):
    title = _("Expansion Slots")
    parameter_name = "expansion_slots"

    LESS_THAN_4 = "lt_4"
    BETWEEN_4_AND_7 = "4_7"
    MORE_THAN_7 = "gt_7"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_4, _("Less than 4")),
            (self.BETWEEN_4_AND_7, _("4 - 7")),
            (self.MORE_THAN_7, _("More than 7")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_4:
            return queryset.filter(number_of_expansion_slots__lt=4)
        elif self.value() == self.BETWEEN_4_AND_7:
            return queryset.filter(number_of_expansion_slots__range=(4, 7))
        elif self.value() == self.MORE_THAN_7:
            return queryset.filter(number_of_expansion_slots__gt=7)


class CaseFrontPanelUSBFilter(admin.SimpleListFilter):
    title = _("Front Panel USB Ports")
    parameter_name = "front_usb"

    # Combine USB 2.0 and 3.x counts for simplicity
    NO_USB = "no_usb"
    ONE_OR_TWO_USB = "1_2_usb"
    THREE_OR_MORE_USB = "3_plus_usb"

    def lookups(self, request, model_admin):
        return (
            (self.NO_USB, _("No USB Ports")),
            (self.ONE_OR_TWO_USB, _("1-2 USB Ports")),
            (self.THREE_OR_MORE_USB, _("3+ USB Ports")),
        )

    def queryset(self, request, queryset):
        total_usb = (
            models.F("usb2_ports_count")
            + models.F("usb3_ports_count")
            + models.F("usb3_1_ports_count")
        )
        if self.value() == self.NO_USB:
            return queryset.filter(total_usb=0)
        elif self.value() == self.ONE_OR_TWO_USB:
            return queryset.filter(total_usb__range=(1, 2))
        elif self.value() == self.THREE_OR_MORE_USB:
            return queryset.filter(total_usb__gte=3)
