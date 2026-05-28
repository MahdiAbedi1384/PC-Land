from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.models import Monitor


# --- Panel Type Filter ---
class MonitorPanelTypeFilter(admin.SimpleListFilter):
    title = _("panel type")
    parameter_name = "panel_type"

    def lookups(self, request, model_admin):
        return Monitor.PanelType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(panel_type=self.value())
        return queryset


# --- Aspect Ratio Filter ---
class MonitorAspectRatioFilter(admin.SimpleListFilter):
    title = _("aspect ratio")
    parameter_name = "aspect_ratio"

    def lookups(self, request, model_admin):
        return Monitor.AspectRatio.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(aspect_ratio=self.value())
        return queryset


# --- Built-in Speakers Filter ---
class MonitorHasSpeakersFilter(admin.SimpleListFilter):
    title = _("has speakers")
    parameter_name = "has_speakers"

    def lookups(self, request, model_admin):
        return [
            ("True", _("Yes")),
            ("False", _("No")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(has_speakers=(self.value() == "True"))
        return queryset


# --- Refresh Rate Filter ---
# This will allow filtering by specific Hz values.
# For more advanced range filtering, a custom filter might be needed.
class MonitorRefreshRateFilter(admin.SimpleListFilter):
    title = _("refresh rate (Hz)")
    parameter_name = "refresh_rate_hz"

    def lookups(self, request, model_admin):
        # You might want to populate this with common refresh rates,
        # or fetch distinct values from the database if there are many.
        # For now, using a few common examples:
        return [
            ("60", _("60Hz")),
            ("75", _("75Hz")),
            ("144", _("144Hz")),
            ("240", _("240Hz")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(refresh_rate_hz=int(self.value()))
        return queryset


# --- Screen Size Filter ---
# Similar to refresh rate, this is a simple filter for exact matches.
# For ranges (e.g., 24-27 inches), a custom filter would be more appropriate.
class MonitorScreenSizeFilter(admin.SimpleListFilter):
    title = _("screen size (inches)")
    parameter_name = "screen_size_inches"

    def lookups(self, request, model_admin):
        # Again, providing common screen sizes.
        return [
            ("21.5", _("21.5 inches")),
            ("23.8", _("23.8 inches")),
            ("27.0", _("27.0 inches")),
            ("31.5", _("31.5 inches")),
            ("34.0", _("34.0 inches")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(screen_size_inches=float(self.value()))
        return queryset


# --- VRR Technology Filter ---
class MonitorVrrTechnologyFilter(admin.SimpleListFilter):
    title = _("VRR technology")
    parameter_name = "vrr_technology"

    def lookups(self, request, model_admin):
        # Fetch distinct VRR technologies from the database for more dynamic options
        # For now, using common examples:
        return [
            ("FreeSync", _("FreeSync")),
            ("G-Sync Compatible", _("G-Sync Compatible")),
            ("G-Sync", _("G-Sync")),
            ("G-Sync Ultimate", _("G-Sync Ultimate")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            # Use case-insensitive search if needed, but for exact matches:
            return queryset.filter(vrr_technology__icontains=self.value())
        return queryset


# --- Brightness Filter ---
# Simple filter for specific brightness levels
class MonitorBrightnessFilter(admin.SimpleListFilter):
    title = _("brightness (nits)")
    parameter_name = "brightness_nits"

    def lookups(self, request, model_admin):
        # Common brightness levels
        return [
            ("300", _("300 nits")),
            ("350", _("350 nits")),
            ("400", _("400 nits")),
            ("500", _("500 nits")),
            ("600", _("600 nits")),
            ("1000", _("1000 nits")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brightness_nits=int(self.value()))
        return queryset
