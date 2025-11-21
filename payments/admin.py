from __future__ import annotations

from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "method", "status", "amount", "currency", "created_at")
    list_filter = ("method", "status", "currency", "created_at")
    search_fields = ("provider_payment_id", "provider_session_id")

