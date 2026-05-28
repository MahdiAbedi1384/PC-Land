from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem, Discount, ReturnRequest, ReturnImage, ReturnItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["content_type", "object_id", "quantity", "price"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "status",
        "total_price",
        "paid_amount",
        "is_paid",
        "delivery_status",
        "created",
    ]

    list_display_links = [
        "id",
        "user",
    ]

    list_filter = [
        "status",
        "created",
    ]

    search_fields = [
        "id",
        "user__username",
        "tracking_code",
        "authority",
    ]

    list_editable = [
        "status",
        "delivery_status",
    ]

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "product",
        "quantity",
        "price",
    ]

    list_display_links = [
        "id",
        "product",
    ]

    search_fields = [
        "order__id",
    ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "discount_type",
        "amount",
        "max_discount_amount",
        "active",
        "used_count",
        "usage_limit",
        "is_expired",
    ]

    list_filter = [
        "discount_type",
        "active",
    ]

    search_fields = [
        "code",
    ]


class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    extra = 0
    readonly_fields = ("order_item", "quantity")
    can_delete = False


class ReturnImageInline(admin.TabularInline):
    model = ReturnImage
    extra = 0
    readonly_fields = ("image_tag",)
    can_delete = False

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url,
            )
        return "-"

    # استفاده از _ برای قابلیت ترجمه
    image_tag.short_description = _("Image Preview")


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "reason", "status", "created_at")
    list_filter = ("status", "reason", "created_at")
    search_fields = (
        "id",
        "order__id",
        "order__tracking_code",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("created_at",)
    list_editable = ("status",)

    inlines = [ReturnItemInline, ReturnImageInline]

    fieldsets = (
        (_("Basic Information"), {"fields": ("order", "user", "created_at")}),
        (_("Request Details"), {"fields": ("reason", "description", "status")}),
    )

    # برای اینکه ادمین‌های عادی نتوانند کل درخواست را اشتباهاً حذف کنند (اختیاری)
    def has_delete_permission(self, request, obj=None):
        return False
