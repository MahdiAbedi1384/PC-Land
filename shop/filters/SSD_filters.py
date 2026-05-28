from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SSDCapacityFilter(admin.SimpleListFilter):
    title = _("Capacity (GB)")
    parameter_name = "capacity"

    # Define common capacity ranges
    UP_TO_256 = "upto_256"
    UP_TO_512 = "upto_512"
    UP_TO_1TB = "upto_1tb"
    MORE_THAN_1TB = "gt_1tb"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_256, _("Up to 256 GB")),
            (self.UP_TO_512, _("Up to 512 GB")),
            (self.UP_TO_1TB, _("Up to 1 TB")),
            (self.MORE_THAN_1TB, _("More than 1 TB")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_256:
            return queryset.filter(capacity__lte=256)
        elif self.value() == self.UP_TO_512:
            return queryset.filter(capacity__lte=512)
        elif self.value() == self.UP_TO_1TB:
            return queryset.filter(capacity__lte=1024)  # Assuming capacity is in GB
        elif self.value() == self.MORE_THAN_1TB:
            return queryset.filter(capacity__gt=1024)


class SSDInterfaceStandardFilter(admin.SimpleListFilter):
    title = _("Interface Standard")
    parameter_name = "internal_ssd_interface_standard"

    def lookups(self, request, model_admin):
        return (
            ("SATA", _("SATA")),
            ("NVMe", _("NVMe")),
            ("PCIe", _("PCIe")),
            ("M.2 SATA", _("M.2 SATA")),
            ("M.2 NVMe", _("M.2 NVMe")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                internal_ssd_interface_standard__icontains=self.value()
            )


class SSDFlashDriveTypeFilter(admin.SimpleListFilter):
    title = _("Flash Drive Type")
    parameter_name = "flash_drive_type"

    def lookups(self, request, model_admin):
        return (
            ("TLC", _("TLC")),
            ("QLC", _("QLC")),
            ("MLC", _("MLC")),
            ("SLC", _("SLC")),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(flash_drive_type__iexact=self.value())


class SSDInterfaceTypeFilter(admin.SimpleListFilter):
    title = _("SSD Interface Type")
    parameter_name = "ssd_interface_type"

    def lookups(self, request, model_admin):
        return (
            ("USB 3.0", _("USB 3.0")),
            ("USB 3.1", _("USB 3.1")),
            ("USB-C", _("USB-C")),
            ("Thunderbolt 3", _("Thunderbolt 3")),
            ("Thunderbolt 4", _("Thunderbolt 4")),
            # Add others if applicable for external SSDs
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ssd_interface_type__icontains=self.value())


class SSDOrderedReadSpeedFilter(admin.SimpleListFilter):
    title = _("Ordered Read Speed (MB/s)")
    parameter_name = "ordered_read_speed"

    # Define common speed tiers
    TIER_500 = "tier_500"
    TIER_1000 = "tier_1000"
    TIER_2000 = "tier_2000"
    TIER_3500 = "tier_3500"  # Common for NVMe
    TIER_7000 = "tier_7000"  # Common for PCIe 4.0 NVMe

    def lookups(self, request, model_admin):
        return (
            (self.TIER_500, _("Up to 500 MB/s")),
            (self.TIER_1000, _("Up to 1000 MB/s")),
            (self.TIER_2000, _("Up to 2000 MB/s")),
            (self.TIER_3500, _("Up to 3500 MB/s")),
            (self.TIER_7000, _("Up to 7000 MB/s")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.TIER_500:
            return queryset.filter(ordered_read_speed__lte=500)
        elif self.value() == self.TIER_1000:
            return queryset.filter(ordered_read_speed__lte=1000)
        elif self.value() == self.TIER_2000:
            return queryset.filter(ordered_read_speed__lte=2000)
        elif self.value() == self.TIER_3500:
            return queryset.filter(ordered_read_speed__lte=3500)
        elif self.value() == self.TIER_7000:
            return queryset.filter(ordered_read_speed__lte=7000)


class SSDOrderedWriteSpeedFilter(admin.SimpleListFilter):
    title = _("Ordered Write Speed (MB/s)")
    parameter_name = "ordered_write_speed"

    # Define common speed tiers - might differ from read speeds
    TIER_400 = "tier_400"
    TIER_800 = "tier_800"
    TIER_1500 = "tier_1500"
    TIER_3000 = "tier_3000"  # Common for NVMe
    TIER_6000 = "tier_6000"  # Common for PCIe 4.0 NVMe

    def lookups(self, request, model_admin):
        return (
            (self.TIER_400, _("Up to 400 MB/s")),
            (self.TIER_800, _("Up to 800 MB/s")),
            (self.TIER_1500, _("Up to 1500 MB/s")),
            (self.TIER_3000, _("Up to 3000 MB/s")),
            (self.TIER_6000, _("Up to 6000 MB/s")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.TIER_400:
            return queryset.filter(ordered_write_speed__lte=400)
        elif self.value() == self.TIER_800:
            return queryset.filter(ordered_write_speed__lte=800)
        elif self.value() == self.TIER_1500:
            return queryset.filter(ordered_write_speed__lte=1500)
        elif self.value() == self.TIER_3000:
            return queryset.filter(ordered_write_speed__lte=3000)
        elif self.value() == self.TIER_6000:
            return queryset.filter(ordered_write_speed__lte=6000)


class SSDAverageLifespanFilter(admin.SimpleListFilter):
    title = _("Average Lifespan (TBW)")
    parameter_name = "average_lifespan"

    # Define common lifespan tiers
    TIER_150TBW = "tier_150tbw"
    TIER_300TBW = "tier_300tbw"
    TIER_600TBW = "tier_600tbw"
    TIER_1200TBW = "tier_1200tbw"
    TIER_2400TBW = "tier_2400tbw"

    def lookups(self, request, model_admin):
        return (
            (self.TIER_150TBW, _("Up to 150 TBW")),
            (self.TIER_300TBW, _("Up to 300 TBW")),
            (self.TIER_600TBW, _("Up to 600 TBW")),
            (self.TIER_1200TBW, _("Up to 1200 TBW")),
            (self.TIER_2400TBW, _("Up to 2400 TBW")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.TIER_150TBW:
            return queryset.filter(average_lifespan__lte=150)
        elif self.value() == self.TIER_300TBW:
            return queryset.filter(average_lifespan__lte=300)
        elif self.value() == self.TIER_600TBW:
            return queryset.filter(average_lifespan__lte=600)
        elif self.value() == self.TIER_1200TBW:
            return queryset.filter(average_lifespan__lte=1200)
        elif self.value() == self.TIER_2400TBW:
            return queryset.filter(average_lifespan__lte=2400)


class SSDFeaturesFilter(admin.SimpleListFilter):
    title = _("SSD Features")
    parameter_name = "ssd_features"

    # Example with predefined features:
    def lookups(self, request, model_admin):
        return (
            ("encryption", _("Hardware Encryption")),
            ("trim_support", _("TRIM Support")),
            ("wear_leveling", _("Wear Leveling")),
            ("raid_support", _("RAID Support")),
        )

    def queryset(self, request, queryset):
        if self.value() == "encryption":
            return queryset.filter(ssd_features__icontains="Hardware Encryption")
        elif self.value() == "trim_support":
            return queryset.filter(ssd_features__icontains="TRIM Support")
        elif self.value() == "wear_leveling":
            return queryset.filter(ssd_features__icontains="Wear Leveling")
        elif self.value() == "raid_support":
            return queryset.filter(ssd_features__icontains="RAID Support")

    #     # ... other features ...

    # For now, rely on the admin's search bar for general text matching.
