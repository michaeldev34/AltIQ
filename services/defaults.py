from __future__ import annotations
from decimal import Decimal
from django.conf import settings
from .models import IndividualService, ServicePackage


def ensure_default_individual_services() -> None:
    """Ensure the four individual AltIQ services exist and are active."""
    services = [
        {"slug": "reporte-estadistico", "name_es": "Reporte Estadístico", "name_en": "Statistical Report",
         "short_description_es": "Análisis de datos con insights accionables.",
         "short_description_en": "Data analysis with actionable insights.",
         "icon": "chart-bar", "price_mxn": Decimal("800"), "is_active": True, "display_order": 1},
        {"slug": "hora-consultoria", "name_es": "Hora de Consultoría", "name_en": "Consulting Hour",
         "short_description_es": "Sesión 1:1 con experto en AI industrial.",
         "short_description_en": "1:1 session with industrial AI expert.",
         "icon": "clock", "price_mxn": Decimal("500"), "is_active": True, "display_order": 2},
        {"slug": "app", "name_es": "Aplicación Web", "name_en": "Web Application",
         "short_description_es": "Herramienta digital a la medida.",
         "short_description_en": "Custom digital tool.",
         "icon": "device-mobile", "price_mxn": Decimal("8000"), "is_active": True, "display_order": 3},
        {"slug": "automatizacion", "name_es": "Solución de Automatización", "name_en": "Automation Solution",
         "short_description_es": "Automatiza procesos repetitivos.",
         "short_description_en": "Automate repetitive processes.",
         "icon": "cog", "price_mxn": Decimal("5000"), "is_active": True, "display_order": 4},
    ]
    env = getattr(settings, "ALTIQ_ENV", "main") or "main"
    if env.strip().lower() in {"test", "testing"}:
        for data in services:
            data["price_mxn"] = Decimal("1")
    for data in services:
        slug = data.pop("slug")
        IndividualService.objects.update_or_create(slug=slug, defaults=data)


def ensure_default_service_packages() -> None:
    """Ensure the three canonical AltIQ service packages exist and are active."""
    packages = [
        {"slug": "basic", "name_es": "Paquete Básico", "name_en": "Basic Package",
         "short_description_es": "Reportes puntuales sobre tu operación y datos clave.",
         "short_description_en": "Focused reports on your operation and key data.",
         "price_mxn": Decimal("500"), "is_active": True, "display_order": 1},
        {"slug": "medium", "name_es": "Paquete Medium", "name_en": "Medium Package",
         "short_description_es": "Diagnóstico profundo y recomendaciones priorizadas.",
         "short_description_en": "Deeper diagnostic and prioritized recommendations.",
         "price_mxn": Decimal("3000"), "is_active": True, "display_order": 2},
        {"slug": "master", "name_es": "Paquete Master", "name_en": "Master Package",
         "short_description_es": "Implementación de una solución digital hecha a la medida.",
         "short_description_en": "Implementation of a custom digital solution.",
         "price_mxn": Decimal("15000"), "is_active": True, "display_order": 3},
    ]
    env = getattr(settings, "ALTIQ_ENV", "main") or "main"
    if env.strip().lower() in {"test", "testing"}:
        for data in packages:
            data["price_mxn"] = Decimal("1")
    for data in packages:
        slug = data.pop("slug")
        ServicePackage.objects.update_or_create(slug=slug, defaults=data)

