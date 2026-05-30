from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            # جست‌وجوی کاربر بر اساس ایمیل یا موبایل
            if "@" in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(phone_number=username)
        except User.DoesNotExist:
            # وجود ندارد → فقط failure معمولی
            return None

        # پسورد اشتباه
        if not user.check_password(password):
            return None

        # # پسورد صحیح → ریست تلاش‌های Axes
        # if request:
        #     reset_request(request)

        return user


class OTPBackend(ModelBackend):
    def authenticate(self, request, phone=None, otp=None, **kwargs):
        if not phone or not otp:
            return None

        key = f"{settings.OTP_REDIS_PREFIX}{phone}"
        real_otp = cache.get(key)

        # OTP منقضی شده یا موجود نیست
        if not real_otp:
            return None

        # OTP غلط
        if otp != real_otp:
            return None

        # پیدا کردن کاربر
        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None

        # # OTP صحیح → ریست Axes
        # if request:
        #     reset_request(request)

        return user
