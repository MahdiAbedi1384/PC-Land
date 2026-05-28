from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import CPUModel


class CpuArchitectureTypeFilter(admin.SimpleListFilter):
    title = _("CPU Architecture Type")
    parameter_name = "cpu_architecture_type"

    def lookups(self, request, model_admin):
        return [
            ("32", _("32-bit")),
            ("64", _("64-bit")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cpu_architecture_type=self.value())


class CPUCoresFilter(admin.SimpleListFilter):
    title = _("Cores")
    parameter_name = "cores"

    LESS_THAN_4 = "<4"
    BETWEEN_4_AND_8 = "4=<8"
    BETWEEN_8_AND_16 = "8=<16"
    MORE_THAN_16 = "16<"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_4, _("Less than 4 cores")),
            (self.BETWEEN_4_AND_8, _("4-8 cores")),
            (self.BETWEEN_8_AND_16, _("8-16 cores")),
            (self.MORE_THAN_16, _("More than 16 cores")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_4:
            return queryset.filter(cores__lt=4)
        elif self.value() == self.BETWEEN_4_AND_8:
            return queryset.filter(cores__range=(4, 8))
        elif self.value() == self.BETWEEN_8_AND_16:
            return queryset.filter(cores__range=(8, 16))
        elif self.value() == self.MORE_THAN_16:
            return queryset.filter(cores__gt=16)


class CPUThreadsFilter(admin.SimpleListFilter):
    title = _("Threads")
    parameter_name = "threads"

    LESS_THAN_8 = "<8"
    BETWEEN_8_AND_16 = "8=<16"
    BETWEEN_16_AND_32 = "16=<32"
    MORE_THAN_32 = "32<"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_8, _("Less than 8 threads")),
            (self.BETWEEN_8_AND_16, _("8-16 threads")),
            (self.BETWEEN_16_AND_32, _("16-32 threads")),
            (self.MORE_THAN_32, _("More than 32 threads")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_8:
            return queryset.filter(threads__lt=8)
        elif self.value() == self.BETWEEN_8_AND_16:
            return queryset.filter(threads__range=(8, 16))
        elif self.value() == self.BETWEEN_16_AND_32:
            return queryset.filter(threads__range=(16, 32))
        elif self.value() == self.MORE_THAN_32:
            return queryset.filter(threads__gt=32)


class CpuGenerationFilter(admin.SimpleListFilter):
    title = _('CPU Generation')
    parameter_name = 'cpu_generation'

    # ✅ استفاده از داده‌های ثابت و مرتب شده
    # این مقادیر باید بر اساس داده‌های موجود در دیتابیس شما تعیین شوند.
    # مثال: اگر نسل‌های 9 تا 14 موجود هستند:
    GENERATION_CHOICES = [
        ('6', _('6th Gen')),
        ('7', _('7th Gen')),
        ('8', _('8th Gen')),
        ('9', _('9th Gen')),
        ('10', _('10th Gen')),
        ('11', _('11th Gen')),
        ('12', _('12th Gen')),
        ('13', _('13th Gen')),
        ('14', _('14th Gen')),
        # ... نسل‌های دیگر را اضافه کنید
    ]

    def lookups(self, request, model_admin):
        # استفاده مستقیم از لیست ثابت
        return self.GENERATION_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            # فیلتر بر اساس مقدار عددی صحیح
            return queryset.filter(cpu_generation=int(self.value()))
        return queryset

class CPUBaseFrequencyFilter(admin.SimpleListFilter):
    title = _("Base Frequency")
    parameter_name = "base_frequency"

    LESS_THAN_2_5_GHZ = "lt_2.5"
    BETWEEN_2_5_AND_3_5_GHZ = "2.5_3.5"
    BETWEEN_3_5_AND_4_5_GHZ = "3.5_4.5"
    MORE_THAN_4_5_GHZ = "gt_4.5"

    def lookups(self, request, model_admin):
        return (
            (self.LESS_THAN_2_5_GHZ, _("Less than 2.5 GHz")),
            (self.BETWEEN_2_5_AND_3_5_GHZ, _("2.5 - 3.5 GHz")),
            (self.BETWEEN_3_5_AND_4_5_GHZ, _("3.5 - 4.5 GHz")),
            (self.MORE_THAN_4_5_GHZ, _("More than 4.5 GHz")),
        )

    def queryset(self, request, queryset):
        if self.value() == self.LESS_THAN_2_5_GHZ:
            # فرض می‌کنیم فرکانس بر حسب گیگاهرتز ذخیره شده
            return queryset.filter(base_frequency__lt=2.5)
        elif self.value() == self.BETWEEN_2_5_AND_3_5_GHZ:
            return queryset.filter(base_frequency__range=(2.5, 3.5))
        elif self.value() == self.BETWEEN_3_5_AND_4_5_GHZ:
            return queryset.filter(base_frequency__range=(3.5, 4.5))
        elif self.value() == self.MORE_THAN_4_5_GHZ:
            return queryset.filter(base_frequency__gt=4.5)


class CPUBrandFilter(admin.SimpleListFilter):
    title = _("Brand")
    parameter_name = "brand"

    # ✅ لیست ثابت برندهای CPU
    # این مقادیر باید یک بار از دیتابیس استخراج شده و سپس در اینجا قرار داده شوند.
    # مثال: فرض کنید برندهای موجود عبارتند از: Intel, AMD, Apple
    CPU_BRAND_CHOICES = [
        ('Intel', 'Intel'),
        ('AMD', 'AMD'),
        ('Apple', 'Apple'),
        # ... برندهای دیگر را اضافه کنید
    ]

    def lookups(self, request, model_admin):
        # استفاده مستقیم از لیست ثابت به جای کوئری دیتابیس
        return self.CPU_BRAND_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            # فیلتر کردن بر اساس مقدار انتخاب شده
            return queryset.filter(brand=self.value())
        return queryset