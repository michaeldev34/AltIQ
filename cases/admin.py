from __future__ import annotations

from django.contrib import admin

from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title_es", "industry", "highlight_metric", "is_featured", "created_at")
    list_filter = ("industry", "is_featured", "created_at")
    prepopulated_fields = {"slug": ("title_es",)}
    search_fields = ("title_es", "industry")

