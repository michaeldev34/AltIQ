from __future__ import annotations

from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("paypal/webhook/", views.paypal_webhook, name="paypal_webhook"),
    path("coinbase/webhook/", views.coinbase_webhook, name="coinbase_webhook"),
]

