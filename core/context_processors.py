from __future__ import annotations

from django.conf import settings


def environment(request):
    """Inject a simple environment flag into all templates.

    The value comes from settings.ALTIQ_ENV, which is controlled via the
    ALTIQ_ENV environment variable ("main", "staging", "test", etc.).
    """

    return {"ALTIQ_ENV": getattr(settings, "ALTIQ_ENV", "main")}
