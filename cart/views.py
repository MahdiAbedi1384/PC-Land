from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from .cart import Cart
from .forms import AddToCartProductForm


class CartAddView(View):
    def post(self, request, app_label, model_name, object_id):
        cart = Cart(request)

        # پیدا کردن مدل با ContentType
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        model_class = content_type.model_class()
        product = get_object_or_404(model_class, id=object_id)

        # فرم
        form = AddToCartProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            cart.add(product=product, quantity=cd["quantity"], replace=cd["replace"])

        return redirect("cart:detail")


class CartRemoveView(View):
    def post(self, request, app_label, model_name, object_id):
        cart = Cart(request)

        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        model_class = content_type.model_class()
        product = get_object_or_404(model_class, id=object_id)

        cart.remove(product)

        return redirect("cart:detail")


class CartDetailView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context


class CartUpdateAjaxView(View):
    def post(self, request, app_label, model_name, object_id):
        cart = Cart(request)

        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        model_class = content_type.model_class()
        product = get_object_or_404(model_class, id=object_id)

        quantity = int(request.POST.get("quantity", 1))

        cart.add(product=product, quantity=quantity, replace=True)

        return JsonResponse(
            {
                "item_total": product.price * quantity,
                "cart_total": cart.get_total_price(),
                "success": True,
            }
        )
