from __future__ import annotations

from django.shortcuts import render

from .models import Expert


def about(request):
    experts = Expert.objects.filter(is_visible=True).order_by("order", "id")
    return render(request, "about/about.html", {"experts": experts})

