from __future__ import annotations

from django.conf import settings


def environment(request):
    """Inject a simple environment flag into all templates."""
    return {"ALTIQ_ENV": getattr(settings, "ALTIQ_ENV", "main")}

