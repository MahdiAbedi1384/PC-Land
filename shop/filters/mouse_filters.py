from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import Mouse


class MouseConnectionTypeFilter(admin.SimpleListFilter):
    title = _("connection type")
    parameter_name = "connection_type"

    def lookups(self, request, model_admin):
        # Use the choices directly from the model's TextChoices
        return Mouse.ConnectionType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(connection_type=self.value())
        return queryset


# --- Sensor Type Filter ---
class MouseSensorTypeFilter(admin.SimpleListFilter):
    title = _("sensor type")
    parameter_name = "sensor_type"

    def lookups(self, request, model_admin):
        return Mouse.SensorType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sensor_type=self.value())
        return queryset


# --- Hand Orientation Filter ---
class MouseHandOrientationFilter(admin.SimpleListFilter):
    title = _("hand orientation")
    parameter_name = "hand_orientation"

    def lookups(self, request, model_admin):
        return Mouse.HandOrientation.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hand_orientation=self.value())
        return queryset


# --- Boolean Filters (for fields like has_scroll_wheel, rgb_lighting, etc.) ---
# These filters will allow you to filter by True/False


class MouseHasScrollWheelFilter(admin.SimpleListFilter):
    title = _("has scroll wheel")
    parameter_name = "has_scroll_wheel"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(has_scroll_wheel=(self.value() == "True"))
        return queryset


class MouseRgbLightingFilter(admin.SimpleListFilter):
    title = _("RGB lighting")
    parameter_name = "rgb_lighting"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rgb_lighting=(self.value() == "True"))
        return queryset


class MouseRechargeableFilter(admin.SimpleListFilter):
    title = _("rechargeable battery")
    parameter_name = "rechargeable"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rechargeable=(self.value() == "True"))
        return queryset


class MouseErgonomicDesignFilter(admin.SimpleListFilter):
    title = _("ergonomic design")
    parameter_name = "ergonomic_design"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ergonomic_design=(self.value() == "True"))
        return queryset


class MouseWaterproofFilter(admin.SimpleListFilter):
    title = _("waterproof")
    parameter_name = "waterproof"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(waterproof=(self.value() == "True"))
        return queryset
