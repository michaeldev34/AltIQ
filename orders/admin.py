from __future__ import annotations

from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "package", "customer_name", "status", "amount", "currency", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("customer_name", "company_name", "email")

