from decimal import Decimal

from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from shop.models import PreBuiltPC


class PreBuiltPCCPUFilter(admin.SimpleListFilter):
    title = _("CPU Model")
    parameter_name = "cpu_model"

    # تعریف لیستی ثابت از CPU های رایج
    # این لیست باید بر اساس داده‌های واقعی شما تنظیم شود.
    CPU_CHOICES = [
        ('intel_i5', _('Intel Core i5')),
        ('intel_i7', _('Intel Core i7')),
        ('intel_i9', _('Intel Core i9')),
        ('amd_r5', _('AMD Ryzen 5')),
        ('amd_r7', _('AMD Ryzen 7')),
        ('amd_r9', _('AMD Ryzen 9')),
        ('other', _('Other CPU')),
    ]

    def lookups(self, request, model_admin):
        return self.CPU_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'intel_i5':
            return queryset.filter(cpu__model__icontains='i5')
        elif value == 'intel_i7':
            return queryset.filter(cpu__model__icontains='i7')
        elif value == 'intel_i9':
            return queryset.filter(cpu__model__icontains='i9')
        elif value == 'amd_r5':
            return queryset.filter(cpu__model__icontains='Ryzen 5')
        elif value == 'amd_r7':
            return queryset.filter(cpu__model__icontains='Ryzen 7')
        elif value == 'amd_r9':
            return queryset.filter(cpu__model__icontains='Ryzen 9')
        elif value == 'other':
            # فیلتر کردن مواردی که در هیچ کدام از دسته‌های بالا نیستند
            return queryset.exclude(
                Q(cpu__model__icontains='i5') |
                Q(cpu__model__icontains='i7') |
                Q(cpu__model__icontains='i9') |
                Q(cpu__model__icontains='Ryzen 5') |
                Q(cpu__model__icontains='Ryzen 7') |
                Q(cpu__model__icontains='Ryzen 9')
            )
        return queryset


class PreBuiltPCMotherboardFilter(admin.SimpleListFilter):
    title = _("Motherboard Model")
    parameter_name = "motherboard_model"

    # تعریف لیستی ثابت از Motherboard های رایج
    MOTHERBOARD_CHOICES = [
        ('intel_chipset_z', _('Intel Z Series Chipset')),
        ('intel_chipset_b', _('Intel B Series Chipset')),
        ('amd_chipset_x', _('AMD X Series Chipset')),
        ('amd_chipset_b', _('AMD B Series Chipset')),
        ('other', _('Other Motherboard')),
    ]

    def lookups(self, request, model_admin):
        return self.MOTHERBOARD_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'intel_chipset_z':
            return queryset.filter(motherboard__model__icontains='Z series')  # مثال
        elif value == 'intel_chipset_b':
            return queryset.filter(motherboard__model__icontains='B series')  # مثال
        elif value == 'amd_chipset_x':
            return queryset.filter(motherboard__model__icontains='X series')  # مثال
        elif value == 'amd_chipset_b':
            return queryset.filter(motherboard__model__icontains='B series')  # مثال
        elif value == 'other':
            return queryset.exclude(
                Q(motherboard__model__icontains='Z series') |
                Q(motherboard__model__icontains='B series') |
                Q(motherboard__model__icontains='X series')
            )
        return queryset


class PreBuiltPCGPUFilter(admin.SimpleListFilter):
    title = _("GPU Model")
    parameter_name = "gpu_model"

    # تعریف لیستی ثابت از GPU های رایج
    GPU_CHOICES = [
        ('nvidia_rtx_40', _('NVIDIA RTX 40 Series')),
        ('nvidia_rtx_30', _('NVIDIA RTX 30 Series')),
        ('nvidia_gtx_16', _('NVIDIA GTX 16 Series')),
        ('amd_rx_7000', _('AMD RX 7000 Series')),
        ('amd_rx_6000', _('AMD RX 6000 Series')),
        ('other', _('Other GPU')),
    ]

    def lookups(self, request, model_admin):
        return self.GPU_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'nvidia_rtx_40':
            return queryset.filter(gpu__model__icontains='RTX 40')
        elif value == 'nvidia_rtx_30':
            return queryset.filter(gpu__model__icontains='RTX 30')
        elif value == 'nvidia_gtx_16':
            return queryset.filter(gpu__model__icontains='GTX 16')
        elif value == 'amd_rx_7000':
            return queryset.filter(gpu__model__icontains='RX 7')
        elif value == 'amd_rx_6000':
            return queryset.filter(gpu__model__icontains='RX 6')
        elif value == 'other':
            return queryset.exclude(
                Q(gpu__model__icontains='RTX 40') |
                Q(gpu__model__icontains='RTX 30') |
                Q(gpu__model__icontains='GTX 16') |
                Q(gpu__model__icontains='RX 7') |
                Q(gpu__model__icontains='RX 6')
            )
        return queryset


class PreBuiltPCCaseFilter(admin.SimpleListFilter):
    title = _("Case Model")
    parameter_name = "case_model"

    # تعریف لیستی ثابت از Case های رایج
    CASE_CHOICES = [
        ('atx_mid_tower', _('ATX Mid-Tower')),
        ('atx_full_tower', _('ATX Full-Tower')),
        ('micro_atx_mini_tower', _('Micro-ATX Mini-Tower')),
        ('sff', _('Small Form Factor (SFF)')),
        ('other', _('Other Case')),
    ]

    def lookups(self, request, model_admin):
        return self.CASE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'atx_mid_tower':
            # فرض می‌کنیم مدل case دارای فیلدی مانند 'type' یا 'size' است
            return queryset.filter(case__name__icontains='Mid-Tower')  # مثال، بسته به نام‌گذاری مدل case
        elif value == 'atx_full_tower':
            return queryset.filter(case__name__icontains='Full-Tower')
        elif value == 'micro_atx_mini_tower':
            return queryset.filter(case__name__icontains='Micro-ATX')
        elif value == 'sff':
            return queryset.filter(case__name__icontains='SFF')
        elif value == 'other':
            return queryset.exclude(
                Q(case__name__icontains='Mid-Tower') |
                Q(case__name__icontains='Full-Tower') |
                Q(case__name__icontains='Micro-ATX') |
                Q(case__name__icontains='SFF')
            )
        return queryset


class PreBuiltPCRamTypeFilter(admin.SimpleListFilter):
    title = _("RAM Type")
    parameter_name = "ram_type"

    # تعریف لیستی ثابت از انواع RAM رایج
    RAM_TYPE_CHOICES = [
        ('ddr4', _('DDR4')),
        ('ddr5', _('DDR5')),
        ('other', _('Other RAM Type')),
    ]

    def lookups(self, request, model_admin):
        return self.RAM_TYPE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'ddr4':
            return queryset.filter(ram_type__title__icontains='DDR4')
        elif value == 'ddr5':
            return queryset.filter(ram_type__title__icontains='DDR5')
        elif value == 'other':
            return queryset.exclude(Q(ram_type__title__icontains='DDR4') | Q(ram_type__title__icontains='DDR5'))
        return queryset


class PreBuiltPCSSDTypeFilter(admin.SimpleListFilter):
    title = _("Internal SSD Type")
    parameter_name = "internal_ssd_type"

    # تعریف لیستی ثابت از انواع SSD رایج
    SSD_TYPE_CHOICES = [
        ('sata_ssd', _('SATA SSD')),
        ('nvme_ssd', _('NVMe SSD')),
        ('other', _('Other SSD Type')),
    ]

    def lookups(self, request, model_admin):
        return self.SSD_TYPE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'sata_ssd':
            return queryset.filter(internal_ssd__flash_drive_type__icontains='SATA')
        elif value == 'nvme_ssd':
            return queryset.filter(internal_ssd__flash_drive_type__icontains='NVMe')
        elif value == 'other':
            return queryset.exclude(Q(internal_ssd__flash_drive_type__icontains='SATA') | Q(
                internal_ssd__flash_drive_type__icontains='NVMe'))
        return queryset


class PreBuiltPCM2SSDTypeFilter(admin.SimpleListFilter):
    title = _("Internal M.2 SSD Type")
    parameter_name = "internal_m2_ssd_type"

    # تعریف لیستی ثابت از انواع M.2 SSD رایج
    M2_SSD_TYPE_CHOICES = [
        ('sata_m2', _('SATA M.2')),
        ('nvme_m2', _('NVMe M.2')),
        ('other', _('Other M.2 SSD Type')),
    ]

    def lookups(self, request, model_admin):
        return self.M2_SSD_TYPE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'sata_m2':
            return queryset.filter(internal_m2_ssd__flash_drive_type__icontains='SATA')
        elif value == 'nvme_m2':
            return queryset.filter(internal_m2_ssd__flash_drive_type__icontains='NVMe')
        elif value == 'other':
            return queryset.exclude(Q(internal_m2_ssd__flash_drive_type__icontains='SATA') | Q(
                internal_m2_ssd__flash_drive_type__icontains='NVMe'))
        return queryset


class PreBuiltPCInternalHDDFilter(admin.SimpleListFilter):
    title = _("Internal HDD Model")
    parameter_name = "internal_hdd_model"

    # تعریف لیستی ثابت از HDD های رایج (بر اساس مدل یا برند)
    HDD_CHOICES = [
        ('hdd_1tb', _('1TB HDD')),
        ('hdd_2tb', _('2TB HDD')),
        ('hdd_4tb', _('4TB HDD')),
        ('other', _('Other HDD')),
    ]

    def lookups(self, request, model_admin):
        return self.HDD_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'hdd_1tb':
            return queryset.filter(internal_hdd__model__icontains='1TB')  # مثال
        elif value == 'hdd_2tb':
            return queryset.filter(internal_hdd__model__icontains='2TB')
        elif value == 'hdd_4tb':
            return queryset.filter(internal_hdd__model__icontains='4TB')
        elif value == 'other':
            return queryset.exclude(
                Q(internal_hdd__model__icontains='1TB') |
                Q(internal_hdd__model__icontains='2TB') |
                Q(internal_hdd__model__icontains='4TB')
            )
        return queryset


# فیلترهای عددی و متنی که نیاز به تعریف لیست ثابت از مقادیر متمایز دارند:

class PreBuiltPCRamCapacityFilter(admin.SimpleListFilter):
    title = _("RAM Capacity (GB)")
    parameter_name = "ram_capacity_gb"

    # این لیست باید یک بار محاسبه و ثابت شود.
    # مثال: RAM_CAPACITY_CHOICES = [(str(c[0]), str(c[0])) for c in PreBuiltPC.objects.values_list('ram_capacity_gb').distinct().order_by('ram_capacity_gb')]
    # برای مثال، فرض می‌کنیم مقادیر زیر رایج هستند:
    RAM_CAPACITY_CHOICES = [
        ('8', _('8GB')),
        ('16', _('16GB')),
        ('32', _('32GB')),
        ('64', _('64GB')),
        ('128', _('128GB')),
        ('other', _('Other Capacity')),
    ]

    def lookups(self, request, model_admin):
        # در حالت ایده‌آل، این لیست باید از یک منبع ثابت یا کش شده خوانده شود.
        # اگر هنوز کوئری می‌زنید، باید به صورت یک‌باره و سپس کش شود.
        # مثال: return [(str(c[0]), str(c[0])) for c in PreBuiltPC.objects.values_list('ram_capacity_gb', flat=True).distinct().order_by('ram_capacity_gb')]
        return self.RAM_CAPACITY_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        try:
            capacity = int(value)
            return queryset.filter(ram_capacity_gb=capacity)
        except (ValueError, TypeError):
            if value == 'other':
                # فیلتر کردن مواردی که در لیست ثابت نیستند
                allowed_capacities = [int(c[0]) for c in self.RAM_CAPACITY_CHOICES if c[0].isdigit()]
                return queryset.exclude(ram_capacity_gb__in=allowed_capacities)
            return queryset  # یا مدیریت خطا به شکل دیگر


class PreBuiltPCPowerSupplyFilter(admin.SimpleListFilter):
    title = _("Power Supply Wattage (W)")
    parameter_name = "power_supply_wattage"

    # این لیست باید یک بار محاسبه و ثابت شود.
    # مثال: PSU_WATTAGE_CHOICES = [(str(c[0]), str(c[0])) for c in PreBuiltPC.objects.values_list('power_supply_wattage').distinct().order_by('power_supply_wattage')]
    PSU_WATTAGE_CHOICES = [
        ('450', _('450W')),
        ('550', _('550W')),
        ('650', _('650W')),
        ('750', _('750W')),
        ('850', _('850W')),
        ('1000', _('1000W')),
        ('other', _('Other Wattage')),
    ]

    def lookups(self, request, model_admin):
        return self.PSU_WATTAGE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        try:
            wattage = int(value)
            return queryset.filter(power_supply_wattage=wattage)
        except (ValueError, TypeError):
            if value == 'other':
                allowed_wattages = [int(c[0]) for c in self.PSU_WATTAGE_CHOICES if c[0].isdigit()]
                return queryset.exclude(power_supply_wattage__in=allowed_wattages)
            return queryset


class PreBuiltPCSalesAudienceFilter(admin.SimpleListFilter):
    title = _("Target Audience")
    parameter_name = "target_audience"

    # این لیست باید یک بار محاسبه و ثابت شود.
    # مثال: SALES_AUDIENCE_CHOICES = [(c, c) for c in PreBuiltPC.objects.values_list('target_audience', flat=True).distinct().order_by('target_audience')]
    SALES_AUDIENCE_CHOICES = [
        ('gaming', _('Gaming')),
        ('professional', _('Professional Use')),
        ('student', _('Student')),
        ('home_office', _('Home Office')),
        ('other', _('Other Audience')),
    ]

    def lookups(self, request, model_admin):
        return self.SALES_AUDIENCE_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'other':
            return queryset.exclude(target_audience__in=[c[0] for c in self.SALES_AUDIENCE_CHOICES if c[0] != 'other'])
        return queryset.filter(target_audience=value)


class PreBuiltPCFormFactorFilter(admin.SimpleListFilter):
    title = _("Form Factor")
    parameter_name = "form_factor"

    # این لیست باید یک بار محاسبه و ثابت شود.
    # مثال: FORM_FACTOR_CHOICES = [(c, c) for c in PreBuiltPC.objects.values_list('form_factor', flat=True).distinct().order_by('form_factor')]
    FORM_FACTOR_CHOICES = [
        ('atx', _('ATX')),
        ('micro_atx', _('Micro-ATX')),
        ('mini_itx', _('Mini-ITX')),
        ('other', _('Other Form Factor')),
    ]

    def lookups(self, request, model_admin):
        return self.FORM_FACTOR_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == 'other':
            return queryset.exclude(form_factor__in=[c[0] for c in self.FORM_FACTOR_CHOICES if c[0] != 'other'])
        return queryset.filter(form_factor=value)
