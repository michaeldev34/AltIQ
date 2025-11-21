from __future__ import annotations

from django.contrib import admin

from .models import CustomQuoteRequest, MeetingRequest


@admin.register(CustomQuoteRequest)
class CustomQuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "email", "created_at")
    search_fields = ("full_name", "company_name", "email")
    list_filter = ("created_at",)


@admin.register(MeetingRequest)
class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "email", "meeting_type", "created_at")
    list_filter = ("meeting_type", "created_at")
    search_fields = ("full_name", "company_name", "email")

