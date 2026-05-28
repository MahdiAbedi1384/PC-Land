from uuid import uuid4

from axes.handlers.proxy import AxesProxyHandler
from axes.utils import reset_request
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.views import generic, View
from iranian_cities.models import Province, City

from shop.models import Favorite
from . import forms
from .forms import CompleteProfileForm, AddressForm
from .functions import send_sms
from .models import CustomUser, Addresses

User = get_user_model()


# TODO: create views for accounts signup,login,logout,change otp number,login & signup with phone number
# Create your views here.
class ProfileView(generic.TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # استفاده از select_related برای کاهش کوئری‌های مربوط به Province، City و User
        context["user_addresses"] = self.request.user.addresses.select_related(
            "province", "city", "user"
        ).all()

        return context


class SignUpView(generic.FormView):
    template_name = "registration/signup.html"
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        cd = form.cleaned_data

        if cd["password1"] != cd["password2"]:
            messages.error(self.request, "Passwords don't match")
            return self.form_invalid(form)

        user = CustomUser.objects.create_user(
            username=uuid4().hex[:30],
            email=cd["email"],
            first_name=cd["first_name"],
            last_name=cd["last_name"],
            gender=cd["gender"],
            phone_number=cd["phone_number"],
            password=cd["password1"],
        )

        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(self.success_url)


class SendOTPView(generic.TemplateView):
    template_name = "registration/login.html"

    def post(self, request):
        phone = request.POST.get("phone_number")
        key = f"{settings.OTP_REDIS_PREFIX}{phone}"

        # بلاک بودن کاربر
        if AxesProxyHandler.is_locked(request, credentials={"username": phone}):
            return render(
                request,
                self.template_name,
                {
                    "error": _(
                        "Too many failed attempts. Your phone number is temporarily locked."
                    )
                },
            )

        # OTP قبلی هنوز زنده است
        if cache.get(key):
            return render(
                request,
                self.template_name,
                {"error": _("The previous code is still valid. Please use it.")},
            )

        # تولید OTP جدید
        otp = get_random_string(6, "0123456789")
        cache.set(key, otp, timeout=settings.OTP_EXPIRE_SECONDS)
        message = f"""
                    کد ورود به سایت لپ تاپ استور:
                    code:{otp}
                    
                    """
        response = send_sms(request, message=message, receptor=phone)
        print("OTP SENT:", otp)  # TODO: ارسال واقعی SMS
        print(response)

        return redirect(f"{reverse_lazy('verify_otp')}?phone={phone}")


class VerifyOTPView(generic.TemplateView):
    template_name = "verify-phone.html"

    def get(self, request):
        phone = request.GET.get("phone")
        return render(request, self.template_name, {"phone": phone})

    def post(self, request):
        phone = request.POST.get("phone")

        # 1) اگر کاربر بلاک باشد → OTP بررسی نمی‌کنیم
        if AxesProxyHandler.is_locked(request, credentials={"username": phone}):
            return render(
                request,
                self.template_name,
                {
                    "phone": phone,
                    "error": _(
                        "Too many failed attempts. Your phone number is temporarily locked."
                    ),
                },
            )

        # 2) دریافت OTP ورودی
        otp_entered = "".join(
            [
                request.POST.get("otp1"),
                request.POST.get("otp2"),
                request.POST.get("otp3"),
                request.POST.get("otp4"),
                request.POST.get("otp5"),
                request.POST.get("otp6"),
            ]
        )

        key = f"{settings.OTP_REDIS_PREFIX}{phone}"
        real_otp = cache.get(key)

        # 3) OTP منقضی
        if not real_otp:
            user_login_failed.send(
                sender=__name__,
                request=request,
                credentials={"username": phone},
            )
            return render(
                request,
                self.template_name,
                {
                    "phone": phone,
                    "error": _("The code has expired. Please request a new one."),
                },
            )

        # 4) OTP اشتباه
        if otp_entered != real_otp:
            user_login_failed.send(
                sender=__name__,
                request=request,
                credentials={"username": phone},
            )
            return render(
                request,
                self.template_name,
                {"phone": phone, "error": _("The code is incorrect. Try again.")},
            )

        # 5) OTP درست → لاگین
        cache.delete(key)

        user, created = User.objects.get_or_create(phone_number=phone)
        if created:
            user.username = phone
            user.phone_verified = True
            user.save()
        elif not user.phone_verified:
            user.phone_verified = True
            user.save()

        # پاکسازی Axes (خیلی مهم)
        reset_request(request)

        user.backend = "accounts.auth_backends.OTPBackend"
        login(request, user)

        return redirect("complete_profile") if not user.first_name else redirect("home")


class CompleteProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "profile_complete.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = CompleteProfileForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"error": _("please complete your profile information")},
            )

        data = form.cleaned_data
        user = request.user

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.nat_code = data["nat_code"]
        user.gender = data["gender"]
        user.save()

        return redirect("home")


class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user

        # جدا کردن نام کامل به دو قسمت
        fullname = request.POST.get("fullname", "").strip()
        if " " in fullname:
            first_name, last_name = fullname.split(" ", 1)
        else:
            first_name, last_name = fullname, ""

        user.first_name = first_name
        user.last_name = last_name
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")
        user.nat_code = request.POST.get("nat_code")

        user.save()
        return redirect("profile")


class AccountSettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "settings.html"


class AccountSettingsUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if not user.check_password(current):
            messages.error(request, _("The current password is incorrect"))
            return redirect("account_settings")

        if new != confirm:
            messages.error(request, _("The confirmation password does not match"))
            return redirect("account_settings")

        user.set_password(new)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, _("The password changed successfully"))
        return redirect("account_settings")


# --- Views for Address Management ---


class ManageAddressesView(LoginRequiredMixin, generic.ListView):
    model = Addresses
    template_name = "addresses.html"  # Or a dedicated addresses template
    context_object_name = "addresses"
    paginate_by = 5  # Example pagination

    def get_queryset(self):
        # Filter addresses for the current logged-in user
        return (
            Addresses.objects.filter(user=self.request.user)
            .order_by("-is_default", "-pk")
            .select_related("user", "city", "province")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        provinces = cache.get("provinces")
        if provinces is None:
            provinces = Province.objects.all()
            cache.set("provinces", provinces)
        # You might want to pass provinces and cities here for the form later
        context["provinces"] = provinces
        return context

    def render_to_response(self, context, **response_kwargs):
        # For AJAX requests, return JSON with the rendered addresses list
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            addresses_html = render_to_string(
                "includes/address_list.html",
                {"addresses": self.object_list, "user": self.request.user},
                self.request,
            )
            return JsonResponse({"addresses_html": addresses_html})
        # For regular requests, render the full page
        return render(self.request, self.template_name, context)


class AddressFormView(LoginRequiredMixin, View):
    """ایجاد و ویرایش آدرس به صورت AJAX (بازگرداندن بخشی از HTML)"""

    def get(self, request, user_id, pk=None, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=user_id)

        if pk:  # حالت ویرایش
            address = get_object_or_404(Addresses, pk=pk, user=user)
            form = AddressForm(instance=address)

            cities = cache.get(f"cities_{address.province_id}")
            if cities is None:
                cities = City.objects.filter(province=address.province)
                cache.set(f"cities_{address.province_id}", cities)

            # نکته حیاتی:
            form.fields["city"].queryset = cities

            is_update = True
        else:  # حالت ایجاد
            address = None
            form = AddressForm()

            cities = City.objects.none()

            # همین هم لازمه
            form.fields["city"].queryset = City.objects.none()

            is_update = False

        context = {
            "form": form,
            "address": address,
            "user": user,
            "cities": cities,
            "is_update": is_update,
        }

        form_html = render_to_string("includes/address_form.html", context, request)
        return JsonResponse({"form_html": form_html})

    def post(self, request, user_id, pk=None, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=user_id)

        if pk:
            address = get_object_or_404(Addresses, pk=pk, user=user)
            form = AddressForm(request.POST, instance=address)
            is_update = True
        else:
            address = None
            form = AddressForm(request.POST)
            is_update = False

        # ست کردن queryset شهرها بر اساس استان انتخاب‌شده
        province_id = request.POST.get("province")
        if province_id:
            cities = City.objects.filter(province_id=province_id)
            form.fields["city"].queryset = cities

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            return JsonResponse({"success": True, "id": obj.id})

        # اگر فرم ارور داشته باشد HTML برگردان
        html = render_to_string(
            "includes/address_form.html",
            {
                "form": form,
                "address": address,
                "user": user,
                "cities": form.fields["city"].queryset,
                "is_update": is_update,
            },
            request,
        )

        return JsonResponse({"success": False, "form_html": html})


class DeleteAddressView(LoginRequiredMixin, generic.DeleteView):
    model = Addresses
    success_url = reverse_lazy("manage_addresses")  # Redirect after success

    def dispatch(self, request, *args, **kwargs):
        # Ensure user can only delete their own addresses
        self.object = get_object_or_404(Addresses, pk=kwargs["pk"], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object.delete()
        # For AJAX requests, return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            messages.success(request, "آدرس با موفقیت حذف شد.")  # Optional message
            return JsonResponse({"success": True})
        return HttpResponseRedirect(self.success_url)

    def get_success_url(self):
        # If AJAX, we don't redirect, but the JS will handle the response
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return None  # Or a dummy URL, JS handles it
        return reverse("manage_addresses")


# --- AJAX View for City List ---


def city_list_ajax(request, province_id):
    province_id = province_id
    cities = cache.get(f"cities_{province_id}")
    if cities is None:
        cities = City.objects.filter(province_id=province_id)
        cache.set(f"cities_{province_id}", cities)

    data = [{"id": c.id, "name": c.name} for c in cities]
    return JsonResponse({"cities": data})


class FavoriteListView(LoginRequiredMixin, generic.ListView):
    model = Favorite
    template_name = "favorites.html"
    context_object_name = "favorites"

    def get_queryset(self, *args, **kwargs):
        return Favorite.objects.filter(user=self.request.user).select_related(
            "content_type"
        )


class FavoriteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Favorite
    success_url = reverse_lazy("favorites")

    def get_queryset(self):
        # فقط اجازه حذف رکوردهای خود کاربر
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # حذف سریع بدون صفحه Confirm
        self.get_object().delete()
        return redirect("favorites")
