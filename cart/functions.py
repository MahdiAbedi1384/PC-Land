from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Cart, CartItem


def save_cart_in_db(user, cart_session):
    """
    Saves the session cart to the database, merging with existing items.
    Handles adding new items and updating quantities.
    """
    db_cart, created = Cart.objects.get_or_create(user=user)

    # Get all current cart items from DB for efficient lookup
    db_items_map = {
        f"{item.content_type_id}:{item.object_id}": item for item in db_cart.items.all()
    }

    for key, item_data in cart_session.cart.items():
        ct_id, obj_id = map(int, key.split(":"))
        quantity = item_data["quantity"]

        if key in db_items_map:
            # Item exists in DB, update quantity
            cart_item = db_items_map[key]
            cart_item.quantity = quantity
            cart_item.save()
            # Remove from map so we know which ones were updated/kept
            del db_items_map[key]
        else:
            # New item, create it
            try:
                CartItem.objects.create(
                    cart=db_cart,
                    content_type_id=ct_id,
                    object_id=obj_id,
                    quantity=quantity,
                )
            except Exception as e:
                # Handle potential issues like invalid content_type/object_id if necessary
                print(f"Error creating CartItem: {e}")

                # Delete items that were in DB but are no longer in session cart
    for key, cart_item in db_items_map.items():
        cart_item.delete()

    # Mark cart as modified in session (optional, good practice)
    if hasattr(cart_session, "session"):
        cart_session.session.modified = True


def remove_cart_item_from_db(user, content_type_id, object_id):
    """Removes a specific item from the user's cart in the database."""
    try:
        db_cart = Cart.objects.get(user=user)
        CartItem.objects.filter(
            cart=db_cart, content_type_id=content_type_id, object_id=object_id
        ).delete()
    except Cart.DoesNotExist:
        pass  # Cart doesn't exist, nothing to remove


def clear_user_cart_in_db(user):
    """Clears all items from the user's cart in the database."""
    try:
        db_cart = Cart.objects.get(user=user)
        db_cart.items.all().delete()
        # Optionally delete the UserCart itself if it's empty and you want to reset it
        # db_cart.delete()
    except Cart.DoesNotExist:
        pass  # Cart doesn't exist, nothing to clear


def load_cart_from_db_to_session(user, session_cart_instance, request):
    """
    Loads items from the database into the session cart.
    Merges DB items with existing session items, respecting quantity limits.
    Returns a message indicating if any quantity exceeded 30.
    """
    message_key = None  # For indicating quantity issues

    try:
        db_cart = Cart.objects.prefetch_related("items__content_type").get(user=user)
    except Cart.DoesNotExist:
        db_cart = None  # No cart in DB, session cart remains as is

    if db_cart:
        # Process items from the database
        for cart_item in db_cart.items.all():
            # Construct the key for session cart lookup
            key = f"{cart_item.content_type_id}:{cart_item.object_id}"

            # Get current quantity from session cart for this item, default to 0
            session_quantity = session_cart_instance.cart.get(key, {}).get(
                "quantity", 0
            )

            # Calculate final quantity, merging DB and session items
            final_quantity = cart_item.quantity + session_quantity

            # Apply quantity limit (max 30)
            if final_quantity > 30:
                message_key = ">30"  # Set message flag
                final_quantity = 30
                messages.warning(
                    request, _(f"Quantity for one or more items was capped at 30.")
                )

            # Use the add method of the session cart to handle updates and messages
            # We set replace_current_quantity=True because we are setting the exact final quantity
            # give_message=False because we handle the overall message here
            try:
                # We need the actual product object to use the session cart's add method
                product_obj = cart_item.content_object
                if product_obj:  # Ensure the object is valid
                    session_cart_instance.add(
                        product=product_obj,
                        quantity=final_quantity,
                        replace=True,  # Replace session quantity with the calculated final quantity
                        give_message=False,  # We handle messaging outside
                    )
                else:
                    # If product_obj is None (e.g., deleted), we might want to clean up the DB entry
                    cart_item.delete()
            except Exception as e:
                print(f"Error adding DB item to session cart: {e}")
                # Optionally delete the problematic DB item if it can't be added to session
                cart_item.delete()

        # After merging, clear the database cart items as they are now in the session
        # This is a common pattern for guest-to-user cart migration
        db_cart.items.all().delete()

        # Ensure session is saved after modifications
    session_cart_instance.save()

    return message_key  # Return the message key if quantity limits were hit


# --- Session Cart Class (Provided Earlier) ---
# from your_cart_module import Cart # Assuming Cart class is in a separate file

# class Cart:
#     ... (Keep the polymorphic Cart class exactly as it was) ...
