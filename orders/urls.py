from __future__ import annotations

from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    # /checkout/<package_slug>/
    path("<slug:package_slug>/", views.checkout, name="checkout"),
    path("success/", views.checkout_success, name="success"),
    path("failure/", views.checkout_failure, name="failure"),

]

