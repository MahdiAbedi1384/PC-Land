from dal import autocomplete
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .models import Province, City


class ProvinceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Province.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        province_id = self.forwarded.get("province")
        if province_id:
            qs = qs.filter(province_id=province_id)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


urlpatterns = [
    path(
        "province-autocomplete/",
        ProvinceAutocomplete.as_view(),
        name="province-autocomplete",
    ),
    path("city-autocomplete/", CityAutocomplete.as_view(), name="city-autocomplete"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("send-otp/", views.SendOTPView.as_view(), name="send_otp"),
    path("verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"),
    path(
        "complete-profile/",
        views.CompleteProfileView.as_view(),
        name="complete_profile",
    ),
    path("settings/", views.AccountSettingsView.as_view(), name="account_settings"),
    path(
        "settings/update/",
        views.AccountSettingsUpdateView.as_view(),
        name="account_settings_update",
    ),
    # Address management URLs
    path("addresses/", views.ManageAddressesView.as_view(), name="manage_addresses"),
    path(
        "addresses/form/<int:user_id>/",
        views.AddressFormView.as_view(),
        name="address_form_create",
    ),
    path(
        "addresses/form/<int:user_id>/<int:pk>/",
        views.AddressFormView.as_view(),
        name="address_form_update",
    ),
    path(
        "addresses/<int:pk>/delete/",
        views.DeleteAddressView.as_view(),
        name="delete_address",
    ),
    path(
        "addresses/cities/<int:province_id>/",
        views.city_list_ajax,
        name="city_list_ajax",
    ),
    # Ajax endpoint for cities
    path("favorites/", views.FavoriteListView.as_view(), name="favorites"),
    path(
        "favorites/remove/<int:pk>/",
        views.FavoriteDeleteView.as_view(),
        name="remove_favorite",
    ),
]
