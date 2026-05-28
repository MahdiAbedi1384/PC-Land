from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.OneToOneField(
        verbose_name=_("user"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    # فیلدهای عمومی برای اتصال به هر مدل محصول
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)

    def __str__(self):
        return f"{self.product} x{self.quantity}"

    def total_price(self):
        # فرض بر اینکه هر مدل دارای فیلد price دارد
        return getattr(self.product, "price", 0) * self.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "content_type", "object_id"], name="unique_cart_product"
            )
        ]
