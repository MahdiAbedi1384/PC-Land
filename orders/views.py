from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.models import Addresses
from cart.cart import Cart
from payment.signals import handle_return_requested
from .models import OrderItem, Order, Discount, ReturnImage, ReturnItem, ReturnRequest


@login_required
def order_create_view(request):
    cart = Cart(request)

    # اگر سبد خرید خالی است
    if len(cart) == 0:
        messages.warning(
            request,
            _("شما نمی‌توانید پرداخت را انجام دهید زیرا سبد خرید شما خالی است."),
        )
        return redirect("cart:detail")

    # =========================================
    # حالت POST: ثبت سفارش
    # =========================================
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        coupon_code = request.POST.get(
            "coupon_code"
        )  # اسمی که در تمپلیت input گذاشته بودیم

        # ۱. بررسی آدرس
        if not address_id:
            messages.error(request, _("لطفاً یک آدرس برای ارسال سفارش انتخاب کنید."))
            return redirect("orders:order_create")

        address = get_object_or_404(Addresses, id=address_id, user=request.user)

        # ۲. بررسی کد تخفیف (با استفاده از متدهای خود مدل Discount)
        discount_obj = None
        if coupon_code:
            discount_obj = Discount.objects.filter(code=coupon_code).first()

            if not discount_obj:
                messages.error(request, _("این کد تخفیف معتبر نیست!"))
                return redirect("orders:order_create")

            if discount_obj.is_expired:
                messages.error(
                    request,
                    _(
                        "متاسفانه زمان یا ظرفیت استفاده از این کد تخفیف به پایان رسیده است."
                    ),
                )
                return redirect("orders:order_create")

        # ۳. محاسبه قیمت‌ها
        cart_total = cart.get_total_price()
        discount_amount = 0

        if discount_obj:
            discount_amount = discount_obj.get_discount_amount(cart_total)

        paid_amount = cart_total - discount_amount

        # ۴. ذخیره در دیتابیس (استفاده از transaction برای جلوگیری از دیتای ناقص)
        with transaction.atomic():
            # ساخت سفارش
            order = Order.objects.create(
                user=request.user,
                address=address,
                total_price=cart_total,
                discount=discount_obj,
                paid_amount=paid_amount,
                status=Order.Status.PENDING,
            )

            # ساخت آیتم‌های سفارش
            # ساخت آیتم‌های سفارش
            for item in cart:
                product = item[
                    "product_obj"
                ]  # <--- تغییر به product_obj بر اساس کلاس Cart شما

                # بررسی اینکه محصول از دیتابیس پاک نشده باشد
                if not product:
                    continue

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=product.price,  # <--- خواندن قیمت از روی خود آبجکت محصول
                )
                product.sku -= item["quantity"]
                product.save()

            # آپدیت تعداد استفاده از کد تخفیف
            if discount_obj:
                discount_obj.used_count += 1
                discount_obj.save()

            # پاک کردن سبد خرید
            cart.clear()

            # ذخیره آیدی سفارش در سشن برای رفتن به درگاه پرداخت
            request.session["order_id"] = order.id

            messages.success(
                request,
                _("سفارش شما با موفقیت ایجاد شد، در حال انتقال به درگاه پرداخت..."),
            )
            return redirect(
                "payment:payment_process_sandbox"
            )  # یا اسم URL درگاه پرداخت خودت

    # =========================================
    # حالت GET: نمایش صفحه فرم و انتخاب آدرس
    # =========================================
    addresses = request.user.addresses.all().order_by("-is_default", "-id")

    context = {
        "cart": cart,
        "addresses": addresses,
    }

    return render(request, "checkout.html", context)


@login_required
def order_history_view(request):
    # به جای datetime_created از created استفاده میکنیم.
    # البته چون در Meta مدل Order از قبل ordering = ("-created",) را تعریف کرده‌ای،
    # حتی نوشتن order_by هم در اینجا اختیاری است.
    orders = Order.objects.filter(user=request.user).order_by("-created")

    context = {"orders": orders}

    return render(request, "order_history.html", context)


@login_required
def order_detail_view(request, order_id):
    # با اضافه کردن '__product' به items، به جنگو می‌گوییم که از طریق GenericForeignKey
    # خود محصولات را هم در یک کوئری جداگانه و بهینه واکشی کند.
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items",
            "items__product",
        ).select_related(
            "address",
            "address__city",
            "address__province",
        ),
        id=order_id,
        user=request.user,
    )

    context = {"order": order, "items": order.items.all()}

    return render(request, "order_detail.html", context)


@login_required
@require_POST
def order_reorder_view(request, order_id):
    # دریافت سفارش متعلق به همین کاربر
    order = get_object_or_404(Order, id=order_id, address__user=request.user)

    # نمونه سازی از کلاس سبد خرید
    cart = Cart(request)

    # اضافه کردن تک‌تک محصولات سفارش قبلی به سبد خرید
    for item in order.items.all():
        # متد add در کلاس Cart شما محصول و تعداد را می‌گیرد
        cart.add(
            product=item.product,
            quantity=item.quantity,
            replace=False,  # به مقادیر فعلی سبد خرید اضافه شود
        )

    messages.success(
        request, "محصولات سفارش قبلی با موفقیت به سبد خرید شما اضافه شدند."
    )

    # ریدایرکت به صفحه سبد خرید (نام url را بر اساس پروژه خود تغییر دهید)
    return redirect("cart:detail")


@login_required
def return_products(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.delivery_status != "delivered":
        messages.error(request, "فقط سفارش‌های تحویل داده شده قابل مرجوعی هستند.")
        return redirect("orders:order_detail", order_id=order.id)

    context = {
        "order": order,
    }

    return render(request, "return_product.html", context)


@login_required
def submit_return_request(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # بررسی امنیتی: فقط سفارش‌های تحویل داده شده قابل مرجوعی هستند
    if order.delivery_status != "delivered":
        messages.error(request, "فقط سفارش‌های تحویل داده شده قابل مرجوعی هستند.")
        return redirect("orders:order_detail", order_id=order.id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        description = request.POST.get("description")
        selected_item_ids = request.POST.getlist("selected_items")

        if not selected_item_ids or not reason:
            messages.error(request, "لطفاً حداقل یک محصول و دلیل مرجوعی را مشخص کنید.")
            return redirect("orders:order_detail", order_id=order.id)

        try:
            # استفاده از تراکنش اتمیک برای یکپارچگی دیتابیس
            with transaction.atomic():
                # ۱. ساخت درخواست اصلی
                return_req = ReturnRequest.objects.create(
                    order=order,
                    user=request.user,
                    reason=reason,
                    description=description,
                )

                # ۲. ذخیره آیتم‌ها
                for item_id in selected_item_ids:
                    quantity_str = request.POST.get(f"quantity_{item_id}")
                    if quantity_str and int(quantity_str) > 0:
                        order_item = get_object_or_404(
                            OrderItem, id=item_id, order=order
                        )
                        quantity = int(quantity_str)

                        if quantity > order_item.quantity:
                            # این خطا باعث لغو کل عملیات (Rollback) می‌شود
                            raise ValueError(
                                f"تعداد مرجوعی برای {order_item.product.name} غیرمجاز است."
                            )

                        ReturnItem.objects.create(
                            return_request=return_req,
                            order_item=order_item,
                            quantity=quantity,
                        )

                # ۳. ذخیره عکس‌های آپلود شده
                images = request.FILES.getlist("return_images")
                for img in images:
                    ReturnImage.objects.create(return_request=return_req, image=img)

            messages.success(
                request, "درخواست مرجوعی شما با موفقیت ثبت شد و در حال بررسی است."
            )
            order.delivery_status = order.DeliveryStatus.RETURNED
            order.save()
            handle_return_requested(request, order=order)
            return redirect("orders:order_detail", order_id=order.id)

        except ValueError as e:
            # مدیریت خطای تعداد غیرمجاز (بدون نیاز به delete دستی)
            messages.error(request, str(e))
            return redirect("orders:order_detail", order_id=order.id)

    # اگر نیاز به صفحه مجزا برای فرم مرجوعی دارید، اینجا رندر کنید
    # در غیر این صورت معمولاً به صفحه جزئیات سفارش هدایت می‌شود
    context = {"order": order}
    return render(request, "order_detail.html", context)
