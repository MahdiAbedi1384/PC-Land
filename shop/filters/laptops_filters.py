from decimal import Decimal

from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from shop.models import Laptop

# --- Display Filters ---


class LaptopScreenSizeFilter(admin.SimpleListFilter):
    title = _("Screen Size (inches)")
    parameter_name = "screen_size_inches"

    # بازه‌های پیشنهادی برای سایز صفحه نمایش
    SCREEN_SIZE_CHOICES = [
        ('10-12', _('10-12 inches')),
        ('13-14', _('13-14 inches')),
        ('15-16', _('15-16 inches')),
        ('17+', _('17 inches and above')),
    ]

    def lookups(self, request, model_admin):
        # دیگر کوئری به دیتابیس نمی‌زنیم، از گزینه‌های ثابت استفاده می‌کنیم
        return self.SCREEN_SIZE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == '10-12':
            return queryset.filter(screen_size_inches__gte=10, screen_size_inches__lte=12.9)
        elif value == '13-14':
            return queryset.filter(screen_size_inches__gte=13, screen_size_inches__lte=14.9)
        elif value == '15-16':
            return queryset.filter(screen_size_inches__gte=15, screen_size_inches__lte=16.9)
        elif value == '17+':
            return queryset.filter(screen_size_inches__gte=17)
        return queryset


class LaptopScreenResolutionFilter(admin.SimpleListFilter):
    title = _("Screen Resolution")
    parameter_name = "screen_resolution"

    # دسته‌بندی رزولوشن‌ها
    RESOLUTION_CHOICES = [
        ('HD', _('HD (1366x768)')),
        ('FHD', _('Full HD (1920x1080)')),
        ('QHD', _('Quad HD (2560x1440)')),
        ('4K', _('4K (3840x2160)')),
        ('Other', _('Other')), # برای مقادیری که در دسته‌بندی‌های بالا نیستند
    ]

    def lookups(self, request, model_admin):
        return self.RESOLUTION_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        # این بخش باید با دقت بیشتری بر اساس فرمت واقعی مقادیر در دیتابیس شما تنظیم شود
        # استفاده از icontains برای انعطاف‌پذیری بیشتر
        if value == 'HD':
            return queryset.filter(Q(screen_resolution__icontains='1366x768') | Q(screen_resolution__icontains='HD'))
        elif value == 'FHD':
            return queryset.filter(Q(screen_resolution__icontains='1920x1080') | Q(screen_resolution__icontains='Full HD'))
        elif value == 'QHD':
            return queryset.filter(Q(screen_resolution__icontains='2560x1440') | Q(screen_resolution__icontains='QHD'))
        elif value == '4K':
            return queryset.filter(Q(screen_resolution__icontains='3840x2160') | Q(screen_resolution__icontains='4K'))
        elif value == 'Other':
            # این قسمت شامل تمام مواردی است که در دسته‌بندی‌های بالا نیستند
            # برای پیاده‌سازی دقیق‌تر، ممکن است لازم باشد لیست تمام مقادیر منحصر به فرد را از دیتابیس بگیرید
            # و سپس مقادیری که در دسته‌بندی‌های بالا نیستند را اینجا فیلتر کنید.
            # فعلاً این بهینه‌سازی را به صورت ساده انجام می‌دهیم.
            return queryset.exclude(
                Q(screen_resolution__icontains='1366x768') | Q(screen_resolution__icontains='HD') |
                Q(screen_resolution__icontains='1920x1080') | Q(screen_resolution__icontains='Full HD') |
                Q(screen_resolution__icontains='2560x1440') | Q(screen_resolution__icontains='QHD') |
                Q(screen_resolution__icontains='3840x2160') | Q(screen_resolution__icontains='4K')
            )
        return queryset


class LaptopRefreshRateFilter(admin.SimpleListFilter):
    title = _("Refresh Rate (Hz)")
    parameter_name = "screen_refresh_rate_hz"

    # بازه‌های پیشنهادی برای نرخ تازه‌سازی
    REFRESH_RATE_CHOICES = [
        ('60', _('60 Hz')),
        ('120', _('120 Hz')),
        ('144', _('144 Hz')),
        ('240+', _('240 Hz and above')),
        ('Other', _('Other')),
    ]

    def lookups(self, request, model_admin):
        return self.REFRESH_RATE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == '60':
            return queryset.filter(screen_refresh_rate_hz=60)
        elif value == '120':
            return queryset.filter(screen_refresh_rate_hz=120)
        elif value == '144':
            return queryset.filter(screen_refresh_rate_hz=144)
        elif value == '240+':
            return queryset.filter(screen_refresh_rate_hz__gte=240)
        elif value == 'Other':
            # مواردی که در دسته‌بندی‌های بالا نیستند
            return queryset.exclude(screen_refresh_rate_hz__in=[60, 120, 144]).filter(screen_refresh_rate_hz__lt=240)
        return queryset


class LaptopPanelTypeFilter(admin.SimpleListFilter):
    title = _("Panel Type")
    parameter_name = "screen_panel_type"

    def lookups(self, request, model_admin):
        # این فیلتر به درستی از choices مدل استفاده می‌کند و نیازی به تغییر ندارد
        return [(c, label) for c, label in Laptop._meta.get_field("screen_panel_type").choices]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(screen_panel_type=self.value())
        return queryset


class LaptopAspectRatioFilter(admin.SimpleListFilter):
    title = _("Aspect Ratio")
    parameter_name = "aspect_ratio"

    def lookups(self, request, model_admin):
        # این فیلتر به درستی از choices مدل استفاده می‌کند و نیازی به تغییر ندارد
        return [(c, label) for c, label in Laptop._meta.get_field("aspect_ratio").choices]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aspect_ratio=self.value())
        return queryset


class LaptopTouchscreenFilter(admin.SimpleListFilter):
    title = _("Touchscreen")
    parameter_name = "touchscreen"

    def lookups(self, request, model_admin):
        # این فیلتر هم به درستی کار می‌کند
        return [("True", _("Yes")), ("False", _("No"))]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(touchscreen=True)
        elif self.value() == "False":
            return queryset.filter(touchscreen=False)
        return queryset


# --- CPU & RAM Filters ---

class LaptopCPUModelFilter(admin.SimpleListFilter):
    title = _("CPU Model")
    parameter_name = "cpu_model_name"

    # دسته‌بندی مدل‌های CPU (مثال: Intel Core i3, i5, i7, i9, AMD Ryzen)
    CPU_MODEL_CHOICES = [
        ('Intel Core i3', _('Intel Core i3')),
        ('Intel Core i5', _('Intel Core i5')),
        ('Intel Core i7', _('Intel Core i7')),
        ('Intel Core i9', _('Intel Core i9')),
        ('AMD Ryzen 3', _('AMD Ryzen 3')),
        ('AMD Ryzen 5', _('AMD Ryzen 5')),
        ('AMD Ryzen 7', _('AMD Ryzen 7')),
        ('AMD Ryzen 9', _('AMD Ryzen 9')),
        ('Other Intel', _('Other Intel')),
        ('Other AMD', _('Other AMD')),
        ('Other', _('Other CPU')),
    ]

    def lookups(self, request, model_admin):
        return self.CPU_MODEL_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Intel Core i3':
            return queryset.filter(cpu_model_name__icontains='Intel Core i3')
        elif value == 'Intel Core i5':
            return queryset.filter(cpu_model_name__icontains='Intel Core i5')
        elif value == 'Intel Core i7':
            return queryset.filter(cpu_model_name__icontains='Intel Core i7')
        elif value == 'Intel Core i9':
            return queryset.filter(cpu_model_name__icontains='Intel Core i9')
        elif value == 'AMD Ryzen 3':
            return queryset.filter(cpu_model_name__icontains='AMD Ryzen 3')
        elif value == 'AMD Ryzen 5':
            return queryset.filter(cpu_model_name__icontains='AMD Ryzen 5')
        elif value == 'AMD Ryzen 7':
            return queryset.filter(cpu_model_name__icontains='AMD Ryzen 7')
        elif value == 'AMD Ryzen 9':
            return queryset.filter(cpu_model_name__icontains='AMD Ryzen 9')
        elif value == 'Other Intel':
            return queryset.filter(cpu_model_name__startswith='Intel').exclude(cpu_model_name__icontains=['Core i3', 'Core i5', 'Core i7', 'Core i9'])
        elif value == 'Other AMD':
            return queryset.filter(cpu_model_name__startswith='AMD').exclude(cpu_model_name__icontains=['Ryzen 3', 'Ryzen 5', 'Ryzen 7', 'Ryzen 9'])
        elif value == 'Other':
             # مواردی که با Intel یا AMD شروع نمی‌شوند
            return queryset.exclude(cpu_model_name__startswith='Intel').exclude(cpu_model_name__startswith='AMD')
        return queryset


class LaptopCPUCoreFilter(admin.SimpleListFilter):
    title = _("CPU Cores")
    parameter_name = "cpu_cores"

    # بازه‌های پیشنهادی برای تعداد هسته‌ها
    CPU_CORE_CHOICES = [
        ('2', _('2')),
        ('4', _('4')),
        ('6', _('6')),
        ('8', _('8')),
        ('10+', _('10+')),
    ]

    def lookups(self, request, model_admin):
        return self.CPU_CORE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                cores = int(value)
                if value == '10+':
                    return queryset.filter(cpu_cores__gte=10)
                else:
                    return queryset.filter(cpu_cores=cores)
            except ValueError:
                return queryset # در صورت بروز خطا، کوئری اصلی را برگردان
        return queryset


class LaptopRAMTypeFilter(admin.SimpleListFilter):
    title = _("RAM Type")
    parameter_name = "ram_type"

    def lookups(self, request, model_admin):
        # این قسمت باید با مقادیر ثابت جایگزین شود یا از طریق یک API داخلی خوانده شود
        # فرض می‌کنیم انواع رایج RAM را داریم: DDR3, DDR4, DDR5
        # اگر ram_type یک ForeignKey به مدل دیگری است، باید از آن مدل مقادیر را بگیریم.
        # در اینجا فرض می‌کنیم ram_type یک فیلد متنی یا از choices است.
        # اگر ForeignKey است، باید از همان روش Laptop._meta.get_field("ram_type").choices استفاده شود.
        # در مثال شما ram_type__id, ram_type__title داشتید، پس ForeignKey است.
        # برای جلوگیری از کوئری، لیست را ثابت تعریف می‌کنیم.
        RAM_TYPE_CHOICES = [
            ('DDR3', _('DDR3')),
            ('DDR4', _('DDR4')),
            ('DDR5', _('DDR5')),
            ('LPDDR3', _('LPDDR3')),
            ('LPDDR4', _('LPDDR4')),
            ('LPDDR4X', _('LPDDR4X')),
            ('LPDDR5', _('LPDDR5')),
            ('Other', _('Other')),
        ]
        return RAM_TYPE_CHOICES
        # اگر ram_type یک ForeignKey به مدل دیگری است و title دارد:
        # return [(r.id, r.title) for r in RamTypeModel.objects.all()] # این کوئری می‌زند، پس نباید استفاده شود.

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            # اگر ram_type ForeignKey است، این فیلتر باید بر اساس ID کار کند
            # اگر value مستقیما ID باشد، فیلتر درست است
            # اگر value نام باشد، باید map شود به ID
            # فرض می‌کنیم value ID است
            return queryset.filter(ram_type__id=value) # یا ram_type=value اگر value ID باشد
        return queryset


class LaptopRAMCapacityFilter(admin.SimpleListFilter):
    title = _("RAM Capacity (GB)")
    parameter_name = "ram_capacity_gb"

    # بازه‌های پیشنهادی برای ظرفیت RAM
    RAM_CAPACITY_CHOICES = [
        ('4', _('4 GB')),
        ('8', _('8 GB')),
        ('12', _('12 GB')),
        ('16', _('16 GB')),
        ('24', _('24 GB')),
        ('32', _('32 GB')),
        ('64+', _('64 GB and above')),
    ]

    def lookups(self, request, model_admin):
        return self.RAM_CAPACITY_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                capacity = int(value)
                if value == '64+':
                    return queryset.filter(ram_capacity_gb__gte=64)
                else:
                    return queryset.filter(ram_capacity_gb=capacity)
            except ValueError:
                return queryset
        return queryset


# --- Storage Filters ---

class LaptopStorageTypeFilter(admin.SimpleListFilter):
    title = _("Primary Storage Type")
    parameter_name = "storage_type"

    def lookups(self, request, model_admin):
        # این فیلتر به درستی از choices مدل استفاده می‌کند
        return [(c, label) for c, label in Laptop._meta.get_field("storage_type").choices]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(storage_type=self.value())
        return queryset


class LaptopStorageCapacityFilter(admin.SimpleListFilter):
    title = _("Primary Storage Capacity (GB)")
    parameter_name = "storage_capacity_gb"

    # بازه‌های پیشنهادی برای ظرفیت حافظه ذخیره‌سازی
    STORAGE_CAPACITY_CHOICES = [
        ('128', _('128 GB')),
        ('256', _('256 GB')),
        ('512', _('512 GB')),
        ('1024', _('1 TB')), # 1024 GB
        ('2048', _('2 TB')), # 2048 GB
        ('4096+', _('4 TB and above')),
    ]

    def lookups(self, request, model_admin):
        return self.STORAGE_CAPACITY_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                capacity = int(value)
                if value == '4096+':
                    return queryset.filter(storage_capacity_gb__gte=4096)
                else:
                    return queryset.filter(storage_capacity_gb=capacity)
            except ValueError:
                return queryset
        return queryset


class LaptopSecondaryStorageTypeFilter(admin.SimpleListFilter):
    title = _("Secondary Storage Type")
    parameter_name = "secondary_storage_type"

    def lookups(self, request, model_admin):
        # این فیلتر به درستی از choices مدل استفاده می‌کند
        return [(c, label) for c, label in Laptop._meta.get_field("secondary_storage_type").choices]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(secondary_storage_type=self.value())
        return queryset


# --- GPU Filters ---

class LaptopGPUModelFilter(admin.SimpleListFilter):
    title = _("GPU Model")
    parameter_name = "gpu_model_name"

    # دسته‌بندی مدل‌های GPU (مثال: NVIDIA GeForce, AMD Radeon, Intel Integrated)
    GPU_MODEL_CHOICES = [
        ('NVIDIA GeForce', _('NVIDIA GeForce')),
        ('NVIDIA Quadro', _('NVIDIA Quadro')),
        ('AMD Radeon', _('AMD Radeon')),
        ('AMD Radeon Pro', _('AMD Radeon Pro')),
        ('Intel UHD Graphics', _('Intel UHD Graphics')),
        ('Intel Iris Xe Graphics', _('Intel Iris Xe Graphics')),
        ('Other', _('Other GPU')),
    ]

    def lookups(self, request, model_admin):
        return self.GPU_MODEL_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'NVIDIA GeForce':
            return queryset.filter(gpu_model_name__icontains='GeForce')
        elif value == 'NVIDIA Quadro':
            return queryset.filter(gpu_model_name__icontains='Quadro')
        elif value == 'AMD Radeon':
            return queryset.filter(gpu_model_name__icontains='Radeon', gpu_model_name__exclude='Radeon Pro')
        elif value == 'AMD Radeon Pro':
            return queryset.filter(gpu_model_name__icontains='Radeon Pro')
        elif value == 'Intel UHD Graphics':
            return queryset.filter(gpu_model_name__icontains='Intel UHD Graphics')
        elif value == 'Intel Iris Xe Graphics':
            return queryset.filter(gpu_model_name__icontains='Intel Iris Xe Graphics')
        elif value == 'Other':
            # مواردی که در دسته‌بندی‌های بالا نیستند
            return queryset.exclude(
                Q(gpu_model_name__icontains='GeForce') |
                Q(gpu_model_name__icontains='Quadro') |
                Q(gpu_model_name__icontains='Radeon') | # این شامل Radeon Pro هم می‌شود
                Q(gpu_model_name__icontains='Intel UHD Graphics') |
                Q(gpu_model_name__icontains='Intel Iris Xe Graphics')
            )
        return queryset


class LaptopIntegratedGraphicsFilter(admin.SimpleListFilter):
    title = _("Integrated Graphics")
    parameter_name = "integrated_graphics"

    def lookups(self, request, model_admin):
        return [("True", _("Yes")), ("False", _("No"))]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(integrated_graphics=True)
        elif self.value() == "False":
            return queryset.filter(integrated_graphics=False)
        return queryset


# --- OS & Battery Filters ---

class LaptopOperatingSystemFilter(admin.SimpleListFilter):
    title = _("Operating System")
    parameter_name = "operating_system_name"

    def lookups(self, request, model_admin):
        # برای جلوگیری از کوئری، لیستی از سیستم‌عامل‌های رایج را تعریف می‌کنیم
        # اگر سیستم‌عامل شما ForeignKey به مدل دیگری است، باید آن مدل را هم اینجا در نظر بگیرید
        OS_CHOICES = [
            ('Windows', _('Windows')),
            ('macOS', _('macOS')),
            ('Linux', _('Linux')),
            ('ChromeOS', _('ChromeOS')),
            ('No OS', _('No OS')),
            ('Other', _('Other OS')),
        ]
        return OS_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Windows':
            return queryset.filter(operating_system_name__title__icontains='Windows')
        elif value == 'macOS':
            return queryset.filter(operating_system_name__title__icontains='macOS')
        elif value == 'Linux':
            return queryset.filter(operating_system_name__title__icontains='Linux')
        elif value == 'ChromeOS':
            return queryset.filter(operating_system_name__title__icontains='ChromeOS')
        elif value == 'No OS':
            # فرض می‌کنیم "No OS" یک مقدار خاص در عنوان یا فیلد مربوطه دارد
            return queryset.filter(operating_system_name=None) # یا فیلتر بر اساس یک مقدار خاص
        elif value == 'Other':
            # سیستم‌عامل‌هایی که در لیست بالا نیستند
            return queryset.exclude(
                Q(operating_system_name__title__icontains='Windows') |
                Q(operating_system_name__title__icontains='macOS') |
                Q(operating_system_name__title__icontains='Linux') |
                Q(operating_system_name__title__icontains='ChromeOS')
            ).exclude(operating_system_name=None) # استثنا کردن حالت No OS
        return queryset


class LaptopOSPreinstalledFilter(admin.SimpleListFilter):
    title = _("OS Pre-installed")
    parameter_name = "os_preinstalled"

    def lookups(self, request, model_admin):
        return [("True", _("Yes")), ("False", _("No"))]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(os_preinstalled=True)
        elif self.value() == "False":
            return queryset.filter(os_preinstalled=False)
        return queryset


# --- Physical & Connectivity Filters ---

class LaptopWeightFilter(admin.SimpleListFilter):
    title = _("Weight (kg)")
    parameter_name = "weight_kg"

    # بازه‌های پیشنهادی برای وزن
    WEIGHT_CHOICES = [
        ('0-1', _('0-1 kg')),
        ('1-1.5', _('1-1.5 kg')),
        ('1.5-2', _('1.5-2 kg')),
        ('2-2.5', _('2-2.5 kg')),
        ('2.5+', _('2.5 kg and above')),
    ]

    def lookups(self, request, model_admin):
        return self.WEIGHT_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0-1':
            return queryset.filter(weight_kg__gte=0, weight_kg__lte=1.0)
        elif value == '1-1.5':
            return queryset.filter(weight_kg__gte=1.0, weight_kg__lte=1.5)
        elif value == '1.5-2':
            return queryset.filter(weight_kg__gte=1.5, weight_kg__lte=2.0)
        elif value == '2-2.5':
            return queryset.filter(weight_kg__gte=2.0, weight_kg__lte=2.5)
        elif value == '2.5+':
            return queryset.filter(weight_kg__gte=2.5)
        return queryset


class LaptopWiFiStandardFilter(admin.SimpleListFilter):
    title = _("Wi-Fi Standard")
    parameter_name = "wireless_wifi"

    # استانداردهای رایج Wi-Fi
    WIFI_CHOICES = [
        ('Wi-Fi 4 (802.11n)', _('Wi-Fi 4 (802.11n)')),
        ('Wi-Fi 5 (802.11ac)', _('Wi-Fi 5 (802.11ac)')),
        ('Wi-Fi 6 (802.11ax)', _('Wi-Fi 6 (802.11ax)')),
        ('Wi-Fi 6E', _('Wi-Fi 6E')),
        ('Wi-Fi 7', _('Wi-Fi 7')),
        ('Other', _('Other')),
    ]

    def lookups(self, request, model_admin):
        return self.WIFI_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Wi-Fi 4 (802.11n)':
            return queryset.filter(wireless_wifi__icontains='802.11n')
        elif value == 'Wi-Fi 5 (802.11ac)':
            return queryset.filter(wireless_wifi__icontains='802.11ac')
        elif value == 'Wi-Fi 6 (802.11ax)':
            return queryset.filter(wireless_wifi__icontains='802.11ax')
        elif value == 'Wi-Fi 6E':
            return queryset.filter(wireless_wifi__icontains='Wi-Fi 6E')
        elif value == 'Wi-Fi 7':
            return queryset.filter(wireless_wifi__icontains='Wi-Fi 7')
        elif value == 'Other':
            # مواردی که در لیست بالا نیستند
             return queryset.exclude(
                Q(wireless_wifi__icontains='802.11n') |
                Q(wireless_wifi__icontains='802.11ac') |
                Q(wireless_wifi__icontains='802.11ax') |
                Q(wireless_wifi__icontains='Wi-Fi 6E') |
                Q(wireless_wifi__icontains='Wi-Fi 7')
            )
        return queryset


class LaptopBluetoothVersionFilter(admin.SimpleListFilter):
    title = _("Bluetooth Version")
    parameter_name = "wireless_bluetooth_version"

    # نسخه‌های رایج بلوتوث
    BT_VERSION_CHOICES = [
        ('4.0', _('Bluetooth 4.0')),
        ('4.1', _('Bluetooth 4.1')),
        ('4.2', _('Bluetooth 4.2')),
        ('5.0', _('Bluetooth 5.0')),
        ('5.1', _('Bluetooth 5.1')),
        ('5.2', _('Bluetooth 5.2')),
        ('5.3', _('Bluetooth 5.3')),
        ('6.0', _('Bluetooth 6.0')),
        ('Other', _('Other')),
    ]

    def lookups(self, request, model_admin):
        return self.BT_VERSION_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == '4.0':
            return queryset.filter(wireless_bluetooth_version__startswith='4.0')
        elif value == '4.1':
            return queryset.filter(wireless_bluetooth_version__startswith='4.1')
        elif value == '4.2':
            return queryset.filter(wireless_bluetooth_version__startswith='4.2')
        elif value == '5.0':
            return queryset.filter(wireless_bluetooth_version__startswith='5.0')
        elif value == '5.1':
            return queryset.filter(wireless_bluetooth_version__startswith='5.1')
        elif value == '5.2':
            return queryset.filter(wireless_bluetooth_version__startswith='5.2')
        elif value == '5.3':
            return queryset.filter(wireless_bluetooth_version__startswith='5.3')
        elif value == '6.0':
            return queryset.filter(wireless_bluetooth_version__startswith='6.0')
        elif value == 'Other':
            # مواردی که در لیست بالا نیستند
             return queryset.exclude(
                Q(wireless_bluetooth_version__startswith='4.0') |
                Q(wireless_bluetooth_version__startswith='4.1') |
                Q(wireless_bluetooth_version__startswith='4.2') |
                Q(wireless_bluetooth_version__startswith='5.0') |
                Q(wireless_bluetooth_version__startswith='5.1') |
                Q(wireless_bluetooth_version__startswith='5.2') |
                Q(wireless_bluetooth_version__startswith='5.3') |
                Q(wireless_bluetooth_version__startswith='6.0')
            )
        return queryset


class LaptopColorFilter(admin.SimpleListFilter):
    title = _("Color Options")
    parameter_name = "color_options"

    def lookups(self, request, model_admin):
        # برای جلوگیری از کوئری، لیستی از رنگ‌های رایج را تعریف می‌کنیم
        # اگر color_options یک ForeignKey به مدل Color است، بهتر است آن مدل را هم اینجا در نظر بگیرید
        COLOR_CHOICES = [
            ('Black', _('Black')),
            ('White', _('White')),
            ('Silver', _('Silver')),
            ('Gray', _('Gray')),
            ('Blue', _('Blue')),
            ('Red', _('Red')),
            ('Green', _('Green')),
            ('Gold', _('Gold')),
            ('Other', _('Other Color')),
        ]
        return COLOR_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Other':
             # اگر رنگ مورد نظر در لیست بالا نیست
             return queryset.exclude(color_options__title__in=['Black', 'White', 'Silver', 'Gray', 'Blue', 'Red', 'Green', 'Gold'])
        elif value:
            # اگر مقدار انتخاب شده در لیست رنگ‌های ثابت است
            return queryset.filter(color_options__title=value)
        return queryset