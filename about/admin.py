from __future__ import annotations

from django.contrib import admin

from .models import Expert


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_es", "is_visible", "order")
    list_filter = ("is_visible",)
    search_fields = ("full_name", "role_es", "role_en")
    ordering = ("order", "id")

