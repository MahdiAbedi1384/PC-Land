from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import ExternalHardDrive, ExternalSSD


class ExternalHardDriveExternalSSDCapacityFilter(admin.SimpleListFilter):
    title = _("Capacity")
    parameter_name = "capacity"

    # Define capacity ranges
    UP_TO_1TB = "upto_1tb"
    UP_TO_2TB = "upto_2tb"
    UP_TO_4TB = "upto_4tb"
    MORE_THAN_4TB = "gt_4tb"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_1TB, _("Up to 1 TB")),
            (self.UP_TO_2TB, _("Up to 2 TB")),
            (self.UP_TO_4TB, _("Up to 4 TB")),
            (self.MORE_THAN_4TB, _("More than 4 TB")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # This is a simplified approach. A more robust solution would parse the string.
            # For now, we'll use string containment which might not be perfectly accurate.
            # Example: "1TB" contains "1TB", "2TB" contains "2TB", etc.
            if self.value() == self.UP_TO_1TB:
                # Filter for capacities that are '1TB' or less (assuming no TB values like '0.5TB')
                return queryset.filter(capacity__in=["1TB"])
            elif self.value() == self.UP_TO_2TB:
                # Filter for '1TB' and '2TB'
                return queryset.filter(capacity__in=["1TB", "2TB"])
            elif self.value() == self.UP_TO_4TB:
                # Filter for '1TB', '2TB', '4TB'
                return queryset.filter(capacity__in=["1TB", "2TB", "4TB"])
            elif self.value() == self.MORE_THAN_4TB:
                # Filter for capacities greater than '4TB' (e.g., '5TB', '8TB')
                # This requires more advanced parsing or a different data type for capacity.
                # For simplicity, let's assume common larger sizes.
                return queryset.filter(
                    capacity__in=["5TB", "6TB", "8TB", "10TB"]
                )  # Adjust as needed
        return None


class ExternalHardDriveConnectionTypeFilter(admin.SimpleListFilter):
    title = _("Connection Type")
    parameter_name = "connection_type"

    def lookups(self, request, model_admin):
        # Use the choices defined in the model's ConnectionType
        return ExternalHardDrive.ConnectionType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(connection_type=self.value())


class ExternalSSDHardDriveWarrantyFilter(admin.SimpleListFilter):
    title = _("Warranty (months)")
    parameter_name = "warranty_months"

    # Define common warranty ranges
    UP_TO_12 = "upto_12"
    UP_TO_24 = "upto_24"
    UP_TO_36 = "upto_36"
    MORE_THAN_36 = "gt_36"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_12, _("Up to 12 Months")),
            (self.UP_TO_24, _("Up to 24 Months")),
            (self.UP_TO_36, _("Up to 36 Months")),
            (self.MORE_THAN_36, _("More than 36 Months")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_12:
            return queryset.filter(warranty_months__lte=12)
        elif self.value() == self.UP_TO_24:
            return queryset.filter(warranty_months__lte=24)
        elif self.value() == self.UP_TO_36:
            return queryset.filter(warranty_months__lte=36)
        elif self.value() == self.MORE_THAN_36:
            return queryset.filter(warranty_months__gt=36)


class ExternalHardDriveExternalSSDWaterproofFilter(admin.SimpleListFilter):
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


# Assuming you have a base filter class for ManyToManyFields, e.g.:
# from .filters import SimpleList_ManyToManyField_Filter
# If not, you'd create a custom filter similar to ConnectionTypeFilter but for ManyToMany.


class MaterialsFilter(admin.SimpleListFilter):
    title = _("Materials")
    parameter_name = "materials"

    # Define common materials if applicable, or fetch distinct values
    def lookups(self, request, model_admin):
        # Example with predefined materials:
        return (
            ("aluminum", _("Aluminum")),
            ("plastic", _("Plastic")),
            ("rubber", _("Rubber")),
            ("steel", _("Steel")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # Case-insensitive search for the material
            return queryset.filter(materials__icontains=self.value())


class ExternalSSDInterfaceTypeFilter(admin.SimpleListFilter):
    title = _("Interface Type")
    parameter_name = "interface"

    def lookups(self, request, model_admin):
        # Use the choices defined in the model's InterfaceType
        return ExternalSSD.InterfaceType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(interface=self.value())


class ExternalSSDMemoryTypeFilter(admin.SimpleListFilter):
    title = _("Memory Type")
    parameter_name = "memory_type"

    def lookups(self, request, model_admin):
        # Use the choices defined in the model's MemoryType
        return ExternalSSD.MemoryType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(memory_type=self.value())


class ExternalSSDReadSpeedFilter(admin.SimpleListFilter):
    title = _("Read Speed (MB/s)")
    parameter_name = "read_speed"

    # Define common read speed ranges
    UP_TO_1000 = "upto_1000"
    UP_TO_2000 = "upto_2000"
    UP_TO_3500 = "upto_3500"
    MORE_THAN_3500 = "gt_3500"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_1000, _("Up to 1000 MB/s")),
            (self.UP_TO_2000, _("Up to 2000 MB/s")),
            (self.UP_TO_3500, _("Up to 3500 MB/s")),
            (self.MORE_THAN_3500, _("More than 3500 MB/s")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_1000:
            return queryset.filter(read_speed__lte=1000)
        elif self.value() == self.UP_TO_2000:
            return queryset.filter(read_speed__lte=2000)
        elif self.value() == self.UP_TO_3500:
            return queryset.filter(read_speed__lte=3500)
        elif self.value() == self.MORE_THAN_3500:
            return queryset.filter(read_speed__gt=3500)


class ExternalSSDWriteSpeedFilter(admin.SimpleListFilter):
    title = _("Write Speed (MB/s)")
    parameter_name = "write_speed"

    # Define common write speed ranges
    UP_TO_900 = "upto_900"
    UP_TO_1800 = "upto_1800"
    UP_TO_3000 = "upto_3000"
    MORE_THAN_3000 = "gt_3000"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_900, _("Up to 900 MB/s")),
            (self.UP_TO_1800, _("Up to 1800 MB/s")),
            (self.UP_TO_3000, _("Up to 3000 MB/s")),
            (self.MORE_THAN_3000, _("More than 3000 MB/s")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_900:
            return queryset.filter(write_speed__lte=900)
        elif self.value() == self.UP_TO_1800:
            return queryset.filter(write_speed__lte=1800)
        elif self.value() == self.UP_TO_3000:
            return queryset.filter(write_speed__lte=3000)
        elif self.value() == self.MORE_THAN_3000:
            return queryset.filter(write_speed__gt=3000)


class ExternalSSDShockproofFilter(admin.SimpleListFilter):
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


class ExternalSSDMaterialsFilter(admin.SimpleListFilter):
    title = _("Materials")
    parameter_name = "materials"

    # Define common materials if applicable, or fetch distinct values
    def lookups(self, request, model_admin):
        # Example with predefined materials:
        return (
            ("aluminum", _("Aluminum")),
            ("plastic", _("Plastic")),
            ("rubber", _("Rubber")),
            ("steel", _("Steel")),
            ("magnesium alloy", _("Magnesium Alloy")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # Case-insensitive search for the material
            return queryset.filter(materials__icontains=self.value())
