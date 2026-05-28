from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class RAMMemoryTypeFilter(admin.SimpleListFilter):
    title = _("RAM Memory Type")
    parameter_name = "ram_memory_type"
    RAM_MEMORY_TYPE_DDR = "DDR"
    RAM_MEMORY_TYPE_DDR2 = "DDR2"
    RAM_MEMORY_TYPE_DDR3 = "ddr3"
    RAM_MEMORY_TYPE_DDR4 = "DDR4"
    RAM_MEMORY_TYPE_DDR5 = "DDR5"
    RAM_MEMORY_TYPE_DDR6 = "DDR6"
    RAM_MEMORY_TYPE_DDR3L = "DDR3l"

    def lookups(self, request, model_admin):
        return (
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR, _("DDR")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR2, _("DDR2")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3, _("DDR3")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3L, _("DDR3L")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR4, _("DDR4")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR5, _("DDR5")),
            (RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR6, _("DDR6")),
        )

    def queryset(self, request, queryset):
        if self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR2:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR2
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3L:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR3L
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR4:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR4
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR5:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR5
            )
        elif self.value() == RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR6:
            return queryset.filter(
                memory_type__title=RAMMemoryTypeFilter.RAM_MEMORY_TYPE_DDR6
            )


class RAMMemorySizeFilter(admin.SimpleListFilter):
    title = _("Memory Size (GB)")
    parameter_name = "memory_size"

    LESS_THAN_4 = "<4"
    BETWEEN_4_AND_8 = "4=<8"
    BETWEEN_8_AND_16 = "8=<16"
    BETWEEN_16_AND_32 = "16=<32"
    MORE_THAN_32 = "32<"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_4, _("Less than 4 GB")),
            (self.BETWEEN_4_AND_8, _("Between 4 and 8 GB")),
            (self.BETWEEN_8_AND_16, _("Between 8 and 16 GB")),
            (self.BETWEEN_16_AND_32, _("Between 16 and 32 GB")),
            (self.MORE_THAN_32, _("More than 32 GB")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_4:
            return queryset.filter(memory_size__lt=4)
        elif self.value() == self.BETWEEN_4_AND_8:
            return queryset.filter(memory_size__range=(4, 8))
        elif self.value() == self.BETWEEN_8_AND_16:
            return queryset.filter(memory_size__range=(8, 16))
        elif self.value() == self.BETWEEN_16_AND_32:
            return queryset.filter(memory_size__range=(16, 32))
        elif self.value() == self.MORE_THAN_32:
            return queryset.filter(memory_size__gt=32)


class RAMFrequencyFilter(admin.SimpleListFilter):
    title = _("Frequency (MHz)")
    parameter_name = "frequency"

    LESS_THAN_2133 = "<2133"
    BETWEEN_2133_AND_2666 = "2133=<2666"
    BETWEEN_2666_AND_3200 = "2666=<3200"
    BETWEEN_3200_AND_4200 = "3200=<4200"
    MORE_THAN_4200 = "4200<"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_2133, _("Less than 2133 MHz")),
            (self.BETWEEN_2133_AND_2666, _("Between 2133 and 2666 MHz")),
            (self.BETWEEN_2666_AND_3200, _("Between 2666 and 3200 MHz")),
            (self.BETWEEN_3200_AND_4200, _("Between 3200 and 4200 MHz")),
            (self.MORE_THAN_4200, _("More than 4200 MHz")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_2133:
            return queryset.filter(frequency__lt=2133)
        elif self.value() == self.BETWEEN_2133_AND_2666:
            return queryset.filter(frequency__range=(2133, 2666))
        elif self.value() == self.BETWEEN_2666_AND_3200:
            return queryset.filter(frequency__range=(2666, 3200))
        elif self.value() == self.BETWEEN_3200_AND_4200:
            return queryset.filter(frequency__range=(3200, 4200))
        elif self.value() == self.MORE_THAN_4200:
            return queryset.filter(frequency__gt=4200)
