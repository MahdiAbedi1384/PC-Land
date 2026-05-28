from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def lockout_response(request, credentials=None):
    return render(
        request,
        "registration/login.html",
        {"error": _("Too many failed attempts. Your account is temporarily locked.")},
        status=429,
    )
