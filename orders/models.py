import random
import string

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Addresses


def generate_discount_code():
    return "".join(
        random.choices(string.digits + string.ascii_letters, k=random.randint(8, 50))
    )


def generate_tracking_code():
    return "".join(random.choices(string.digits, k=random.randint(8, 16)))


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", _("Percentage")
        FIXED = "fixed", _("Fixed amount")

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Code"),
        default=generate_discount_code,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
        verbose_name=_("Discount type"),
    )

    amount = models.PositiveIntegerField(verbose_name=_("Amount"))

    max_discount_amount = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Maximum discount amount")
    )

    valid_from = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Valid from")
    )

    valid_to = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid to"))

    active = models.BooleanField(default=True, verbose_name=_("Active"))

    usage_limit = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Usage limit")
    )

    used_count = models.PositiveIntegerField(default=0, verbose_name=_("Used count"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return self.code

    @property
    def is_expired(self):
        now = timezone.now()

        if self.valid_from and now < self.valid_from:
            return True

        if self.valid_to and now > self.valid_to:
            return True

        if not self.active:
            return True

        if self.usage_limit and self.used_count >= self.usage_limit:
            return True

        return False

    def get_discount_amount(self, total_price):
        if self.discount_type == self.DiscountType.PERCENTAGE:
            discount = total_price * self.amount // 100

            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)

        else:
            discount = self.amount

        return min(discount, total_price)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        CANCELED = "canceled", _("Canceled")
        REFUNDED = "refunded", _("Refunded")

    class DeliveryStatus(models.TextChoices):
        PREPARING = "preparing", _("preparing")
        SHIPPED = "shipped", _("shipped")
        DELIVERED = "delivered", _("delivered")
        RETURNED = "returned", _("returned")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name=_("User"),
    )

    address = models.ForeignKey(
        Addresses, on_delete=models.PROTECT, verbose_name=_("Address")
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Order status"),
    )

    delivery_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PREPARING,
        verbose_name=_("Delivery status"),
    )

    total_price = models.PositiveIntegerField(default=0, verbose_name=_("Total price"))

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name=_("Discount"),
    )

    paid_amount = models.PositiveIntegerField(default=0, verbose_name=_("Paid amount"))

    gateway_name = models.CharField(
        max_length=50, blank=True, verbose_name=_("Payment gateway")
    )

    authority = models.CharField(
        max_length=255, blank=True, verbose_name=_("Gateway authority")
    )

    # فیلد جدید برای ذخیره کد پیگیری زرین‌پال
    gateway_ref_id = models.CharField(
        max_length=255, blank=True, verbose_name=_("gateway refid")
    )

    tracking_code = models.CharField(
        max_length=255, default=generate_tracking_code, verbose_name=_("Tracking code")
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def is_paid(self):
        return self.status == self.Status.PAID

    def get_items_total(self):
        from django.db.models import F, Sum

        result = self.items.aggregate(total=Sum(F("price") * F("quantity")))

        return result["total"] or 0

    def recalculate_totals(self, save=True):
        items_total = self.get_items_total()
        self.total_price = items_total

        if self.discount:
            discount_amount = self.discount.get_discount_amount(items_total)
            self.paid_amount = items_total - discount_amount
        else:
            self.paid_amount = items_total

        if save:
            self.save(update_fields=["total_price", "paid_amount"])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order")
    )

    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, verbose_name=_("Product type")
    )

    object_id = models.PositiveIntegerField(verbose_name=_("Product id"))

    product = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name=_("Quantity")
    )

    price = models.PositiveIntegerField(verbose_name=_("Unit price"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    @property
    def item_total(self):
        return self.quantity * self.price


class ReturnRequest(models.Model):
    class Status(models.TextChoices):
        pending = "Pending", _("Pending")
        accepted = "Accepted", _("Accepted")
        rejected = "Rejected", _("Rejected")

    RETURN_REASONS = (
        ("defect", "خرابی محصول"),
        ("wrong_item", "ارسال اشتباه"),
        ("change_mind", "تغییر نظر"),
        ("damaged_package", "بسته‌بندی آسیب دیده"),
        ("other", "سایر دلایل"),
    )

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="returns",
        verbose_name=_("order"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user")
    )
    reason = models.CharField(
        max_length=50, choices=RETURN_REASONS, verbose_name=_("reason")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    status = models.CharField(
        max_length=50,
        default=Status.pending,
        verbose_name=_("status"),
        choices=Status.choices,
    )  # pending, approved, rejected
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    def __str__(self):
        return f"Return Request #{self.id} for Order #{self.order.id}"


class ReturnItem(models.Model):
    return_request = models.ForeignKey(
        ReturnRequest, on_delete=models.CASCADE, related_name="items"
    )
    order_item = models.ForeignKey(
        "OrderItem", on_delete=models.CASCADE, verbose_name=_("ordered item")
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    def __str__(self):
        return f"{self.quantity} x {self.order_item.product.name}"


class ReturnImage(models.Model):
    return_request = models.ForeignKey(
        ReturnRequest, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="returns/%Y/%m/%d/", verbose_name=_("image"))

    def __str__(self):
        return f"Image for Return #{self.return_request.id}"
