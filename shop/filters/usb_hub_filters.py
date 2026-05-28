from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class USBHUBPortsCountFilter(admin.SimpleListFilter):
    title = _("Number of Ports")
    parameter_name = "ports_count"

    # Define common port count ranges
    UP_TO_4 = "upto_4"
    UP_TO_7 = "upto_7"
    UP_TO_10 = "upto_10"
    MORE_THAN_10 = "gt_10"

    def lookups(self, request, model_admin):
        return (
            (self.UP_TO_4, _("Up to 4 Ports")),
            (self.UP_TO_7, _("Up to 7 Ports")),
            (self.UP_TO_10, _("Up to 10 Ports")),
            (self.MORE_THAN_10, _("More than 10 Ports")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.UP_TO_4:
            return queryset.filter(ports_count__lte=4)
        elif self.value() == self.UP_TO_7:
            return queryset.filter(ports_count__lte=7)
        elif self.value() == self.UP_TO_10:
            return queryset.filter(ports_count__lte=10)
        elif self.value() == self.MORE_THAN_10:
            return queryset.filter(ports_count__gt=10)


class USBHUBInterfacesFilter(admin.SimpleListFilter):
    title = _("Interfaces")
    parameter_name = "interfaces"

    def lookups(self, request, model_admin):
        # Define common interface types. Adjust based on actual data or expected values.
        return (
            ("USB 3.0", _("USB 3.0")),
            ("USB 3.1", _("USB 3.1")),
            ("USB-C", _("USB-C")),
            ("Thunderbolt 3", _("Thunderbolt 3")),
            ("Thunderbolt 4", _("Thunderbolt 4")),
        )

    def queryset(self, request, queryset):
        if self.value():
            # Using __icontains for partial matches, or __exact for exact matches
            return queryset.filter(interfaces__icontains=self.value())


# Assuming 'OperationSystemsSupported' is a model with a 'name' field
# You'll need to import OperationSystemsSupported if it's a separate model
# from .models import OperationSystemsSupported


class USBHUBExternalHardDriveCompatibleOperationSystemsFilter(admin.SimpleListFilter):
    """
    Custom filter for ManyToMany field 'compatible_operation_systems'.
    Optimized to use fixed choices and avoid database queries in lookups.
    Assumes 'compatible_operation_systems' is a text-based field storing OS names.
    """

    title = _("Compatible OS")  # Title shown in the admin interface
    parameter_name = "compatible_operation_systems"  # URL parameter for the filter

    # تعریف لیستی از سیستم‌عامل‌های رایج به صورت ثابت
    COMPATIBLE_OS_CHOICES = [
        ('Windows', _('Windows')),
        ('macOS', _('macOS')),
        ('Linux', _('Linux')),
        ('Android', _('Android')),
        ('iOS', _('iOS')),
        ('ChromeOS', _('ChromeOS')),
        ('No OS', _('No OS')), # برای مواردی که سیستم‌عامل خاصی ذکر نشده
        ('Other', _('Other OS')), # برای سایر سیستم‌عامل‌ها
    ]

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples for the filter dropdown using fixed choices.
        Each tuple is (value, label).
        """
        # دیگر کوئری به دیتابیس نمی‌زنیم، از لیست ثابت استفاده می‌کنیم
        return self.COMPATIBLE_OS_CHOICES

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected value.
        Assumes 'compatible_operation_systems' is a text field.
        """
        value = self.value()
        if value:
            if value == 'No OS':
                # فیلتر کردن مواردی که فیلد خالی یا None است
                return queryset.filter(compatible_operation_systems__isnull=True) | \
                       queryset.filter(compatible_operation_systems__exact='')
            elif value == 'Other':
                # فیلتر کردن مواردی که در لیست ثابت نیستند (با استفاده از icontains)
                # این بخش ممکن است نیاز به تنظیم دقیق‌تری داشته باشد
                # بستگی به فرمت دقیق ذخیره شدن نام سیستم‌عامل‌ها در فیلد متنی دارد
                return queryset.exclude(
                    Q(compatible_operation_systems__icontains='Windows') |
                    Q(compatible_operation_systems__icontains='macOS') |
                    Q(compatible_operation_systems__icontains='Linux') |
                    Q(compatible_operation_systems__icontains='Android') |
                    Q(compatible_operation_systems__icontains='iOS') |
                    Q(compatible_operation_systems__icontains='ChromeOS')
                ).filter(compatible_operation_systems__isnull=False).filter(compatible_operation_systems__exact!='').filter(~Q(compatible_operation_systems__icontains='No OS')) # استثنا کردن No OS و موارد خالی
            else:
                # فیلتر بر اساس مقادیر ثابت با استفاده از icontains برای انعطاف‌پذیری
                return queryset.filter(compatible_operation_systems__icontains=value)
        return queryset


class USBHubFeaturesFilter(admin.SimpleListFilter):
    title = _("USB HUB Features")
    parameter_name = "usb_hub_features"

    # This filter is a bit more dynamic.
    # You might pre-define common features or fetch them dynamically if they are standardized.
    # For a simple text search, you can let the user type in the search bar.
    # If you want selectable options, you'd need to parse common features or have a predefined list.

    # Example using predefined features:
    def lookups(self, request, model_admin):
        return (
            ("power_delivery", _("Power Delivery")),
            ("hdmi_output", _("HDMI Output")),
            ("ethernet_port", _("Ethernet Port")),
        )

    def queryset(self, request, queryset):
        if self.value() == "power_delivery":
            return queryset.filter(usb_hub_features__icontains="Power Delivery")
        elif self.value() == "hdmi_output":
            return queryset.filter(usb_hub_features__icontains="HDMI Output")
        elif self.value() == "ethernet_port":
            return queryset.filter(usb_hub_features__icontains="Ethernet Port")

    # For a more general search, you'd rely on the admin's built-in search functionality
    # or implement a custom search filter if needed.
    # For now, we'll leave this as a placeholder and rely on the main search bar.
    # If specific features are common, you can add them as lookup options.
