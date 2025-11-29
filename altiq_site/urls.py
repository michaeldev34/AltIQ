"""URL configuration for the AltIQ project."""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("cases/", include("cases.urls")),
    path("about/", include("about.urls")),
    path("contact/", include("contacts.urls")),
    path("checkout/", include("orders.urls")),
    path("payments/", include("payments.urls")),
]

