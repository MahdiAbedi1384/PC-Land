from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class MotherBoardCPUSocketFilter(admin.SimpleListFilter):
    title = _("CPU Socket Type")
    parameter_name = "cpu_socket"

    def lookups(self, request, model_admin):
        # Assuming cpu_socket_type is a CharField with distinct values
        # You might want to fetch unique values from the database if they are very dynamic
        # For now, let's assume common types. Adjust as needed.
        return (
            ("LGA1700", _("LGA 1700")),
            ("AM5", _("AM5")),
            ("LGA1200", _("LGA 1200")),
            ("AM4", _("AM4")),
            # Add more as per your data
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cpu_socket_type__iexact=self.value())


class MotherBoardChipsetFilter(admin.SimpleListFilter):
    title = _("Chipset")
    parameter_name = "chipset"

    def lookups(self, request, model_admin):
        # Similar to CPU socket, consider fetching unique values if dynamic
        return (
            ("Z790", _("Z790")),
            ("B760", _("B760")),
            ("X670E", _("X670E")),
            ("B650", _("B650")),
            # Add more as per your data
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chipset__iexact=self.value())


class MotherBoardMemorySlotsFilter(admin.SimpleListFilter):
    title = _("Memory Slots")
    parameter_name = "memory_slots"

    def lookups(self, request, model_admin):
        return (
            ("2", _("2 Slots")),
            ("4", _("4 Slots")),
            ("6", _("6 Slots")),  # Less common, but possible
            ("8", _("8 Slots")),  # For server/workstation boards
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(memory_slots=int(self.value()))


class MotherBoardMaxMemoryFilter(admin.SimpleListFilter):
    title = _("Max Memory Supported (GB)")
    parameter_name = "max_memory"

    # Define ranges in GB
    UP_TO_64 = "upto_64"
    UP_TO_128 = "upto_128"
    UP_TO_256 = "upto_256"
    MORE_THAN_256 = "gt_256"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_64, _("Up to 64 GB")),
            (self.UP_TO_128, _("Up to 128 GB")),
            (self.UP_TO_256, _("Up to 256 GB")),
            (self.MORE_THAN_256, _("More than 256 GB")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_64:
            return queryset.filter(max_memory_supported__lte=64)
        elif self.value() == self.UP_TO_128:
            return queryset.filter(max_memory_supported__lte=128)
        elif self.value() == self.UP_TO_256:
            return queryset.filter(max_memory_supported__lte=256)
        elif self.value() == self.MORE_THAN_256:
            return queryset.filter(max_memory_supported__gt=256)


# Assuming RAMTypesSupported has choices or distinct names
class MotherBoardMemoryTypesFilter(admin.SimpleListFilter):
    title = _("Memory Type")
    parameter_name = "memory_type"

    def lookups(self, request, model_admin):
        # Fetch unique RAM types supported across all motherboards
        # This requires a slightly more complex setup, or you can pre-define common ones
        # For simplicity, let's assume common types:
        return (
            ("DDR4", _("DDR4")),
            ("DDR5", _("DDR5")),
            ("DDR5_EXPO", _("DDR5 (EXPO)")),  # Example for specific profiles
            ("DDR5_XMP", _("DDR5 (XMP)")),
            # Add others like DDR3 if relevant for older boards
        )

    def queryset(self, request, queryset):
        if self.value():
            # This filters based on the related model's name/value
            return queryset.filter(
                memory_types_supported__title__icontains=self.value()
            )


class MotherBoardPCIeX16Filter(admin.SimpleListFilter):
    title = _("PCIe x16 Slots")
    parameter_name = "pcie_x16"

    # Define ranges for common needs
    NO_X16 = "0"
    ONE_X16 = "1"
    TWO_X16 = "2"
    THREE_OR_MORE_X16 = "3_plus"

    def lookups(self, request, model_admin):
        return (
            (self.NO_X16, _("0")),
            (self.ONE_X16, _("1")),
            (self.TWO_X16, _("2")),
            (self.THREE_OR_MORE_X16, _("3+")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.NO_X16:
            return queryset.filter(PCI_express_x16_slots_count=0)
        elif self.value() == self.ONE_X16:
            return queryset.filter(PCI_express_x16_slots_count=1)
        elif self.value() == self.TWO_X16:
            return queryset.filter(PCI_express_x16_slots_count=2)
        elif self.value() == self.THREE_OR_MORE_X16:
            return queryset.filter(PCI_express_x16_slots_count__gte=3)


class MotherBoardM2ConnectorsFilter(admin.SimpleListFilter):
    title = _("M.2 Connectors")
    parameter_name = "m2_connectors"

    NO_M2 = "0"
    ONE_M2 = "1"
    TWO_M2 = "2"
    THREE_OR_MORE_M2 = "3_plus"

    def lookups(self, request, model_admin):
        return (
            (self.NO_M2, _("0")),
            (self.ONE_M2, _("1")),
            (self.TWO_M2, _("2")),
            (self.THREE_OR_MORE_M2, _("3+")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.NO_M2:
            return queryset.filter(m2_connectors_count=0)
        elif self.value() == self.ONE_M2:
            return queryset.filter(m2_connectors_count=1)
        elif self.value() == self.TWO_M2:
            return queryset.filter(m2_connectors_count=2)
        elif self.value() == self.THREE_OR_MORE_M2:
            return queryset.filter(m2_connectors_count__gte=3)


class MotherBoardM2SlotTypeFilter(admin.SimpleListFilter):
    title = _("M.2 Slot Type")
    parameter_name = "m2_slot_type"

    def lookups(self, request, model_admin):
        # Common types: NVMe, SATA, PCIe
        return (
            ("NVMe", _("NVMe")),
            ("SATA", _("SATA")),
            ("PCIe", _("PCIe")),  # Often NVMe uses PCIe
            ("PCIe 4.0", _("PCIe 4.0")),
            ("PCIe 5.0", _("PCIe 5.0")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(m2_slot_type__icontains=self.value())


class MotherBoardSATA3Filter(admin.SimpleListFilter):
    title = _("SATA 3.0 Connectors")
    parameter_name = "sata3_connectors"

    # Define ranges
    FOUR_OR_LESS = "4_or_less"
    FIVE_TO_SIX = "5_6"
    SEVEN_OR_MORE = "7_plus"

    def lookups(self, request, model_admin):
        return (
            (self.FOUR_OR_LESS, _("4 or less")),
            (self.FIVE_TO_SIX, _("5-6")),
            (self.SEVEN_OR_MORE, _("7+")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.FOUR_OR_LESS:
            return queryset.filter(sata_3_connectors_count__lte=4)
        elif self.value() == self.FIVE_TO_SIX:
            return queryset.filter(sata_3_connectors_count__range=(5, 6))
        elif self.value() == self.SEVEN_OR_MORE:
            return queryset.filter(sata_3_connectors_count__gte=7)


class MotherBoardUSBTypeCFilter(admin.SimpleListFilter):
    title = _("USB Type-C Ports")
    parameter_name = "usb_type_c"

    NO_TYPE_C = "0"
    ONE_TYPE_C = "1"
    TWO_TYPE_C = "2"
    MORE_THAN_TWO_TYPE_C = "3_plus"

    def lookups(self, request, model_admin):
        return (
            (self.NO_TYPE_C, _("0")),
            (self.ONE_TYPE_C, _("1")),
            (self.TWO_TYPE_C, _("2")),
            (self.MORE_THAN_TWO_TYPE_C, _("3+")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.NO_TYPE_C:
            return queryset.filter(usb_type_c_prots_count=0)
        elif self.value() == self.ONE_TYPE_C:
            return queryset.filter(usb_type_c_prots_count=1)
        elif self.value() == self.TWO_TYPE_C:
            return queryset.filter(usb_type_c_prots_count=2)
        elif self.value() == self.MORE_THAN_TWO_TYPE_C:
            return queryset.filter(usb_type_c_prots_count__gte=3)


class MotherBoardUSB32Gen2Filter(admin.SimpleListFilter):
    title = _("USB 3.2 Gen 2 Ports")
    parameter_name = "usb32_gen2"

    # Similar structure to Type-C filter, adjust counts as needed
    NO_GEN2 = "0"
    ONE_GEN2 = "1"
    TWO_GEN2 = "2"
    THREE_OR_MORE_GEN2 = "3_plus"

    def lookups(self, request, model_admin):
        return (
            (self.NO_GEN2, _("0")),
            (self.ONE_GEN2, _("1")),
            (self.TWO_GEN2, _("2")),
            (self.THREE_OR_MORE_GEN2, _("3+")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.NO_GEN2:
            return queryset.filter(usb_3_p_2_gen2_prots_count=0)
        elif self.value() == self.ONE_GEN2:
            return queryset.filter(usb_3_p_2_gen2_prots_count=1)
        elif self.value() == self.TWO_GEN2:
            return queryset.filter(usb_3_p_2_gen2_prots_count=2)
        elif self.value() == self.THREE_OR_MORE_GEN2:
            return queryset.filter(usb_3_p_2_gen2_prots_count__gte=3)


class MotherBoardFormFactorFilter(admin.SimpleListFilter):
    title = _("Form Factor")
    parameter_name = "form_factor"

    # Common form factors
    ATX = "atx"
    MICRO_ATX = "micro_atx"
    MINI_ITX = "mini_itx"
    E_ATX = "e_atx"

    def lookups(self, request, model_admin):
        return (
            (self.ATX, _("ATX")),
            (self.MICRO_ATX, _("Micro-ATX")),
            (self.MINI_ITX, _("Mini-ITX")),
            (self.E_ATX, _("E-ATX")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(form_factor__icontains=self.value())


class MotherBoardRAIDTypesFilter(admin.SimpleListFilter):
    title = _("RAID Support")
    parameter_name = "raid_type"

    def lookups(self, request, model_admin):
        # Fetch unique RAID types or define common ones
        return (
            ("RAID 0", _("RAID 0")),
            ("RAID 1", _("RAID 1")),
            ("RAID 5", _("RAID 5")),
            ("RAID 10", _("RAID 10")),
            # Add others as needed
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(raid_types_supported__title__icontains=self.value())
