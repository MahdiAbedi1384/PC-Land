from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import FlashDrive


class FlashDriveCapacityFilter(admin.SimpleListFilter):
    title = _("Capacity")
    parameter_name = "capacity"

    # Define common capacity ranges
    UP_TO_32GB = "upto_32gb"
    UP_TO_64GB = "upto_64gb"
    UP_TO_128GB = "upto_128gb"
    UP_TO_256GB = "upto_256gb"
    MORE_THAN_256GB = "gt_256gb"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_32GB, _("Up to 32 GB")),
            (self.UP_TO_64GB, _("Up to 64 GB")),
            (self.UP_TO_128GB, _("Up to 128 GB")),
            (self.UP_TO_256GB, _("Up to 256 GB")),
            (self.MORE_THAN_256GB, _("More than 256 GB")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # This is a simplified approach. A more robust solution would parse the string.
            if self.value() == self.UP_TO_32GB:
                return queryset.filter(capacity__in=["32GB"])
            elif self.value() == self.UP_TO_64GB:
                return queryset.filter(capacity__in=["32GB", "64GB"])
            elif self.value() == self.UP_TO_128GB:
                return queryset.filter(capacity__in=["32GB", "64GB", "128GB"])
            elif self.value() == self.UP_TO_256GB:
                return queryset.filter(capacity__in=["32GB", "64GB", "128GB", "256GB"])
            elif self.value() == self.MORE_THAN_256GB:
                # Add common larger capacities if they exist in your data
                return queryset.filter(
                    capacity__in=["512GB", "1TB"]
                )  # Adjust as needed
        return None


class FlashDriveConnectionTypeFilter(admin.SimpleListFilter):
    title = _("Connection Type")
    parameter_name = "connection_type"

    def lookups(self, request, model_admin):
        # Use the choices defined in the model's ConnectionType
        return FlashDrive.ConnectionType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(connection_type=self.value())


class FlashDriveMaterialFilter(admin.SimpleListFilter):
    title = _("Material")
    parameter_name = "material"

    def lookups(self, request, model_admin):
        # You can predefine common materials or fetch distinct values from the database
        # Example with predefined materials:
        return (
            ("metal", _("Metal")),
            ("plastic", _("Plastic")),
            ("aluminum", _("Aluminum")),
            ("rubber", _("Rubber")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # Case-insensitive search for the material
            return queryset.filter(material__icontains=self.value())


class FlashDriveReadSpeedFilter(admin.SimpleListFilter):
    title = _("Read Speed (MB/s)")
    parameter_name = "read_speed"

    # Define common read speed ranges
    UP_TO_100 = "upto_100"
    UP_TO_500 = "upto_500"
    UP_TO_1000 = "upto_1000"
    MORE_THAN_1000 = "gt_1000"
    NOT_SPECIFIED = "not_specified"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_100, _("Up to 100 MB/s")),
            (self.UP_TO_500, _("Up to 500 MB/s")),
            (self.UP_TO_1000, _("Up to 1000 MB/s")),
            (self.MORE_THAN_1000, _("More than 1000 MB/s")),
            (self.NOT_SPECIFIED, _("Not Specified")),
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.UP_TO_100:
                return queryset.filter(read_speed__lte=100)
            elif self.value() == self.UP_TO_500:
                return queryset.filter(read_speed__lte=500)
            elif self.value() == self.UP_TO_1000:
                return queryset.filter(read_speed__lte=1000)
            elif self.value() == self.MORE_THAN_1000:
                return queryset.filter(read_speed__gt=1000)
            elif self.value() == self.NOT_SPECIFIED:
                return queryset.filter(read_speed__isnull=True)


class FlashDriveWriteSpeedFilter(admin.SimpleListFilter):
    title = _("Write Speed (MB/s)")
    parameter_name = "write_speed"

    # Define common write speed ranges
    UP_TO_50 = "upto_50"
    UP_TO_200 = "upto_200"
    UP_TO_500 = "upto_500"
    MORE_THAN_500 = "gt_500"
    NOT_SPECIFIED = "not_specified"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_50, _("Up to 50 MB/s")),
            (self.UP_TO_200, _("Up to 200 MB/s")),
            (self.UP_TO_500, _("Up to 500 MB/s")),
            (self.MORE_THAN_500, _("More than 500 MB/s")),
            (self.NOT_SPECIFIED, _("Not Specified")),
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.UP_TO_50:
                return queryset.filter(write_speed__lte=50)
            elif self.value() == self.UP_TO_200:
                return queryset.filter(write_speed__lte=200)
            elif self.value() == self.UP_TO_500:
                return queryset.filter(write_speed__lte=500)
            elif self.value() == self.MORE_THAN_500:
                return queryset.filter(write_speed__gt=500)
            elif self.value() == self.NOT_SPECIFIED:
                return queryset.filter(write_speed__isnull=True)


class FlashDriveWaterproofFilter(admin.SimpleListFilter):
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


class FlashDriveShockproofFilter(admin.SimpleListFilter):
    title = _("Shockproof")
    parameter_name = "shockproof"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(shockproof=True)
        elif self.value() == "no":
            return queryset.filter(shockproof=False)


class HardwareEncryptionFilter(admin.SimpleListFilter):
    title = _("Hardware Encryption")
    parameter_name = "hardware_encryption"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(hardware_encryption=True)
        elif self.value() == "no":
            return queryset.filter(hardware_encryption=False)
