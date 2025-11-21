from __future__ import annotations

from django.contrib import admin

from .models import ServicePackage


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ("name_es", "price_mxn", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name_es", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_es",)}
    ordering = ("display_order", "id")

