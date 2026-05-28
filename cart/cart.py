from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Cart:
    """
    A fully generic Session‑based cart supporting unlimited product models.
    Uses ContentType to safely store items from 17+ different product models.
    """

    # ------------------------------------------------------------------
    # INIT: load cart from session + preload all product objects once
    # ------------------------------------------------------------------
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}

        # cart = {
        #   "ctid:objectid": {
        #       "quantity": 3,
        #       "content_type": 12,
        #       "object_id": 40
        #   }
        # }
        self.cart = cart
        self.products = self._load_products_once()

    # ------------------------------------------------------------------
    # Load all product objects referenced in cart (ONE QUERY PER MODEL)
    # ------------------------------------------------------------------
    def _load_products_once(self):
        product_map = {}

        for key, item in self.cart.items():
            ct_id = item["content_type"]
            obj_id = item["object_id"]

            try:
                ct = ContentType.objects.get_for_id(ct_id)
                model = ct.model_class()
                product = model.objects.get(id=obj_id)
                product_map[key] = product

            except Exception:
                continue  # If product deleted from DB, ignore

        return product_map

    # ------------------------------------------------------------------
    # Add or update item quantity
    # replace=False → add to existing quantity
    # replace=True  → set exact quantity
    # ------------------------------------------------------------------
    def add(self, product, quantity=1, replace=False, give_message=True):
        ct = ContentType.objects.get_for_model(product)
        key = f"{ct.id}:{product.id}"

        # Create if missing
        if key not in self.cart:
            self.cart[key] = {
                "quantity": 0,
                "content_type": ct.id,
                "object_id": product.id,
            }

        # Replace quantity
        if replace:
            if quantity < 1:
                messages.error(self.request, _("Quantity cannot be less than 1"))
                return
            if quantity > 30:
                messages.error(self.request, _("Max quantity is 30"))
                return

            self.cart[key]["quantity"] = quantity
            if give_message:
                messages.success(self.request, _("Product quantity updated"))
            self.save()
            return

        # Increase quantity
        new_qty = self.cart[key]["quantity"] + quantity

        if not isinstance(new_qty, int):
            messages.error(self.request, _("Invalid quantity"))
            return

        if new_qty < 1:
            messages.error(self.request, _("Quantity cannot be less than 1"))
            return

        if new_qty > 30:
            messages.error(self.request, _("Max quantity is 30"))
            return

        self.cart[key]["quantity"] = new_qty
        if give_message:
            messages.success(self.request, _("Product added to cart"))

        self.save()

    # ------------------------------------------------------------------
    # Save session
    # ------------------------------------------------------------------
    def save(self):
        self.session.modified = True

    # ------------------------------------------------------------------
    # Remove item
    # ------------------------------------------------------------------
    def remove(self, product):
        ct = ContentType.objects.get_for_model(product)
        key = f"{ct.id}:{product.id}"

        if key in self.cart:
            del self.cart[key]
            messages.success(self.request, _("Product removed from cart"))
            self.save()

    # ------------------------------------------------------------------
    # Iterate through cart items (inject product_obj & totals)
    # ------------------------------------------------------------------
    def __iter__(self):
        for key, item in self.cart.items():
            item_copy = item.copy()

            product_obj = self.products.get(key)
            if product_obj:
                item_copy["product_obj"] = product_obj
                item_copy["total_price"] = product_obj.price * item_copy["quantity"]
                item_copy["total_weight"] = product_obj.weight * item_copy["quantity"]

            yield item_copy

    # ------------------------------------------------------------------
    # Support: `product in cart`
    # ------------------------------------------------------------------
    def __contains__(self, product):
        ct = ContentType.objects.get_for_model(product)
        key = f"{ct.id}:{product.id}"
        return key in self.cart

    # ------------------------------------------------------------------
    # Return total quantity of items in cart
    # ------------------------------------------------------------------
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    # ------------------------------------------------------------------
    # Remove everything
    # ------------------------------------------------------------------
    def clear(self):
        self.session["cart"] = {}
        self.save()

    # ------------------------------------------------------------------
    # Sum of all item prices
    # ------------------------------------------------------------------
    def get_total_price(self):
        return sum(item["total_price"] for item in self)

    # ------------------------------------------------------------------
    def is_empty(self):
        return len(self.cart) == 0
