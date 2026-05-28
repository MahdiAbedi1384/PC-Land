from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import AllInOnePC

# --- AllInOnePC Filters ---


class AllInOnePCScreenSizeFilter(admin.SimpleListFilter):
    title = _("Screen Size (inches)")
    parameter_name = "screen_size_inches"

    # ✅ لیست ثابت سایزهای صفحه نمایش (بر اساس داده‌های موجود قبلی)
    # این مقادیر باید یک بار از دیتابیس استخراج شوند و سپس اینجا قرار داده شوند.
    # مثال: فرض کنید داده‌های شما این‌ها هستند: 18.5, 21.5, 23.8, 27.0
    SCREEN_SIZE_CHOICES = [
        ('18.5', '18.5"'),
        ('21.5', '21.5"'),
        ('23.8', '23.8"'),
        ('27.0', '27.0"'),
        # ... مقادیر دیگر را اینجا اضافه کنید
    ]

    def lookups(self, request, model_admin):
        # استفاده مستقیم از لیست ثابت
        return self.SCREEN_SIZE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            # تبدیل مقدار فیلتر شده به Decimal برای مقایسه با دیتابیس
            return queryset.filter(screen_size_inches=Decimal(self.value()))
        return queryset

# --- Screen Resolution Filter ---
class AllInOnePCScreenResolutionFilter(admin.SimpleListFilter):
    title = _("Screen Resolution")
    parameter_name = "screen_resolution"

    # ✅ لیست ثابت رزولوشن‌های صفحه نمایش (بر اساس داده‌های موجود قبلی)
    # مثال: فرض کنید داده‌های شما این‌ها هستند: "Full HD", "2K", "4K"
    SCREEN_RESOLUTION_CHOICES = [
        ('1920x1080', 'Full HD (1920x1080)'),
        ('2560x1440', 'QHD / 2K (2560x1440)'),
        ('3840x2160', 'UHD / 4K (3840x2160)'),
        # ... مقادیر دیگر را اینجا اضافه کنید
    ]

    def lookups(self, request, model_admin):
        # استفاده مستقیم از لیست ثابت
        return self.SCREEN_RESOLUTION_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(screen_resolution=self.value())
        return queryset

# --- Screen Type Filter (No change needed) ---
class AllInOnePCScreenTypeFilter(admin.SimpleListFilter):
    title = _("Screen Type")
    parameter_name = "screen_type"

    def lookups(self, request, model_admin):
        return [
            (choice, label)
            for choice, label in AllInOnePC._meta.get_field("screen_type").choices
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(screen_type=self.value())
        return queryset

# --- Touchscreen Filter (No change needed) ---
class AllInOnePCTouchscreenFilter(admin.SimpleListFilter):
    title = _("Touchscreen Support")
    parameter_name = "touchscreen"

    def lookups(self, request, model_admin):
        return [("True", _("Yes")), ("False", _("No"))]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(touchscreen=True)
        elif self.value() == "False":
            return queryset.filter(touchscreen=False)
        return queryset

class AllInOnePCRefreshRateFilter(admin.SimpleListFilter):
    title = _("Refresh Rate (Hz)")
    parameter_name = "refresh_rate_hz"

    def lookups(self, request, model_admin):
        rates = AllInOnePC.objects.values_list("refresh_rate_hz").distinct()
        valid_rates = sorted([r[0] for r in rates if r[0] is not None])
        return [(rate, f"{rate} Hz") for rate in valid_rates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(refresh_rate_hz=self.value())
        return queryset


class AllInOnePCCPUModelFilter(admin.SimpleListFilter):
    title = _("CPU Model")
    parameter_name = "cpu_model_name"

    def lookups(self, request, model_admin):
        cpus = AllInOnePC.objects.values_list("cpu_model_name").distinct()
        valid_cpus = sorted([c[0] for c in cpus if c[0]])
        return [(cpu, cpu) for cpu in valid_cpus]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cpu_model_name=self.value())
        return queryset


class AllInOnePCRamTypeFilter(admin.SimpleListFilter):
    title = _("RAM Type")
    parameter_name = "ram_type"

    def lookups(self, request, model_admin):
        ram_types = AllInOnePC.objects.values_list(
            "ram_type__id", "ram_type__title"
        ).distinct()
        return [(rt_id, rt_name) for rt_id, rt_name in ram_types if rt_name]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ram_type__id=self.value())
        return queryset


class AllInOnePCRamCapacityFilter(admin.SimpleListFilter):
    title = _("RAM Capacity (GB)")
    parameter_name = "ram_capacity_gb"

    def lookups(self, request, model_admin):
        rams = AllInOnePC.objects.values_list("ram_capacity_gb").distinct()
        valid_rams = sorted([r[0] for r in rams if r[0] is not None])
        return [(ram, f"{ram} GB") for ram in valid_rams]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ram_capacity_gb=self.value())
        return queryset


class AllInOnePCStorageTypeFilter(admin.SimpleListFilter):
    title = _("Storage Type")
    parameter_name = "storage_type"

    def lookups(self, request, model_admin):
        return [
            (choice, label)
            for choice, label in AllInOnePC._meta.get_field("storage_type").choices
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(storage_type=self.value())
        return queryset


class AllInOnePCStorageCapacityFilter(admin.SimpleListFilter):
    title = _("Storage Capacity (GB)")
    parameter_name = "storage_capacity_gb"

    def lookups(self, request, model_admin):
        capacities = AllInOnePC.objects.values_list("storage_capacity_gb").distinct()
        valid_caps = sorted([c[0] for c in capacities if c[0] is not None])
        return [(cap, f"{cap} GB") for cap in valid_caps]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(storage_capacity_gb=self.value())
        return queryset


class AllInOnePCGPUModelFilter(admin.SimpleListFilter):
    title = _("GPU Model")
    parameter_name = "gpu_model_name"

    def lookups(self, request, model_admin):
        gpus = AllInOnePC.objects.values_list("gpu_model_name").distinct()
        valid_gpus = sorted([g[0] for g in gpus if g[0]])
        return [(gpu, gpu) for gpu in valid_gpus]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(gpu_model_name=self.value())
        return queryset


class AllInOnePCOperatingSystemFilter(admin.SimpleListFilter):
    title = _("Operating System")
    parameter_name = "operating_system"

    def lookups(self, request, model_admin):
        os_list = AllInOnePC.objects.values_list(
            "operating_system__id", "operating_system__title"
        ).distinct()
        return [(os_id, os_name) for os_id, os_name in os_list if os_name]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(operating_system__id=self.value())
        return queryset


class AllInOnePCWebcamFilter(admin.SimpleListFilter):
    title = _("Built-in Webcam")
    parameter_name = "has_webcam"

    def lookups(self, request, model_admin):
        return [("True", _("Yes")), ("False", _("No"))]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(has_webcam=True)
        elif self.value() == "False":
            return queryset.filter(has_webcam=False)
        return queryset


class AllInOnePCColorFilter(admin.SimpleListFilter):
    title = _("Colors")
    parameter_name = "colors"

    def lookups(self, request, model_admin):
        color_list = AllInOnePC.objects.values_list(
            "colors__id", "colors__title"
        ).distinct()
        return [(cid, cname) for cid, cname in color_list if cname]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(colors__id=self.value())
        return queryset


class AllInOnePCWirelessConnectivityFilter(admin.SimpleListFilter):
    title = _("Wireless Connectivity")
    parameter_name = "wireless_connectivity"

    def lookups(self, request, model_admin):
        connections = AllInOnePC.objects.values_list("wireless_connectivity").distinct()
        valid_cons = sorted([c[0] for c in connections if c[0]])
        return [(con, con) for con in valid_cons]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(wireless_connectivity=self.value())
        return queryset
