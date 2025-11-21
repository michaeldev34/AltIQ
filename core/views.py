from __future__ import annotations

from django.shortcuts import render


def home(request):
    """AltIQ main landing page with the full SI-piloted hero."""
    return render(request, "core/landing.html")

