from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm, AddressForm
from .models import CustomUser, Addresses


@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ["id", "user", "province", "city", "is_default"]


class AddressesInline(admin.StackedInline):
    form = AddressForm
    model = Addresses
    search_fields = ["province__name", "city__name"]
    extra = 1  # تعداد فرم‌های خالی برای افزودن آدرس جدید


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ["id", "username", "email", "phone_number"]
    list_display_links = ["id", "username", "email", "phone_number"]
    inlines = (AddressesInline,)
    # list_display = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    # list_display_links = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "gender",
                    "first_name",
                    "last_name",
                    "nat_code",
                    "phone_number",
                    "phone_verified",
                    "email",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "nat_code",
                    "phone_number",
                    "phone_verified",
                    "email",
                ),
            },
        ),
    )
