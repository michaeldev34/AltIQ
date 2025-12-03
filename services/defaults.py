from __future__ import annotations

from decimal import Decimal

from django.conf import settings

from .models import IndividualService, ServicePackage


def ensure_default_individual_services() -> None:
    """Ensure the four individual AltIQ services exist and are active."""

    services = [
        {
            "slug": "reporte-estadistico",
            "name_es": "Reporte Estadístico",
            "name_en": "Statistical Report",
            "short_description_es": "Análisis de datos con insights accionables.",
            "short_description_en": "Data analysis with actionable insights.",
            "description_es": (
                "Recibe un reporte detallado con visualizaciones claras, "
                "tendencias y recomendaciones basadas en tus datos operativos."
            ),
            "description_en": "Detailed report with clear visualizations and recommendations.",
            "icon": "chart-bar",
            "price_mxn": Decimal("800"),
            "is_active": True,
            "display_order": 1,
        },
        {
            "slug": "hora-consultoria",
            "name_es": "Hora de Consultoría",
            "name_en": "Consulting Hour",
            "short_description_es": "Sesión 1:1 con experto en AI industrial.",
            "short_description_en": "1:1 session with industrial AI expert.",
            "description_es": (
                "Una hora de asesoría personalizada para resolver dudas, "
                "evaluar proyectos o definir estrategia de datos."
            ),
            "description_en": "One hour of personalized consulting.",
            "icon": "clock",
            "price_mxn": Decimal("500"),
            "is_active": True,
            "display_order": 2,
        },
        {
            "slug": "app",
            "name_es": "Aplicación Web",
            "name_en": "Web Application",
            "short_description_es": "Herramienta digital a la medida.",
            "short_description_en": "Custom digital tool.",
            "description_es": (
                "Desarrollo de una aplicación web enfocada en un problema "
                "específico de tu operación: dashboards, formularios, reportes."
            ),
            "description_en": "Custom web app for a specific operational problem.",
            "icon": "device-mobile",
            "price_mxn": Decimal("8000"),
            "is_active": True,
            "display_order": 3,
        },
        {
            "slug": "automatizacion",
            "name_es": "Solución de Automatización",
            "name_en": "Automation Solution",
            "short_description_es": "Automatiza procesos repetitivos.",
            "short_description_en": "Automate repetitive processes.",
            "description_es": (
                "Diseño e implementación de flujos automatizados: extracción de datos, "
                "notificaciones, sincronización entre sistemas."
            ),
            "description_en": "Design and implementation of automated workflows.",
            "icon": "cog",
            "price_mxn": Decimal("5000"),
            "is_active": True,
            "display_order": 4,
        },
    ]

    env = getattr(settings, "ALTIQ_ENV", "main") or "main"
    env_normalized = env.strip().lower()
    if env_normalized in {"test", "testing"}:
        for data in services:
            data["price_mxn"] = Decimal("1")

    for data in services:
        slug = data.pop("slug")
        IndividualService.objects.update_or_create(slug=slug, defaults=data)


def ensure_default_service_packages() -> None:
    """Ensure the three canonical AltIQ service packages exist and are active.

    This is idempotent and safe to call on every request. It mirrors the data
    seeded in the `0002_default_packages` migration so that even if that
    migration has not run in a given environment, the /services/ page will
    still show the correct three packages.
    """

    packages = [
        {
            "slug": "basic",
            "name_es": "Paquete Básico",
            "name_en": "Basic Package",
            "short_description_es": "Reportes puntuales sobre tu operación y datos clave.",
            "short_description_en": "Focused reports on your operation and key data.",
            "description_es": (
                "Primer acercamiento para entender tu línea, capturar datos y "
                "detectar oportunidades inmediatas sin fricción."
            ),
            "description_en": (
                "Initial engagement to understand your line, capture data and "
                "detect quick-win opportunities."
            ),
            "price_mxn": Decimal("500"),
            "is_active": True,
            "display_order": 1,
        },
        {
            "slug": "medium",
            "name_es": "Paquete Medium",
            "name_en": "Medium Package",
            "short_description_es": "Diagnóstico profundo y recomendaciones priorizadas.",
            "short_description_en": "Deeper diagnostic and prioritized recommendations.",
            "description_es": (
                "Analizamos variabilidad, cuellos de botella y escenarios "
                "financieros para reducir desperdicio y mejorar flujo."
            ),
            "description_en": (
                "We analyze variability, bottlenecks and financial scenarios to "
                "reduce waste and improve flow."
            ),
            "price_mxn": Decimal("3000"),
            "is_active": True,
            "display_order": 2,
        },
        {
            "slug": "master",
            "name_es": "Paquete Master",
            "name_en": "Master Package",
            "short_description_es": "Implementación de una solución digital hecha a la medida.",
            "short_description_en": "Implementation of a custom digital solution.",
            "description_es": (
                "Incluye el diagnóstico Medium más el desarrollo de un producto "
                "web enfocado en un problema específico de tu planta."
            ),
            "description_en": (
                "Includes the Medium diagnostic plus a web product focused on a "
                "specific problem in your plant."
            ),
            "price_mxn": Decimal("15000"),
            "is_active": True,
            "display_order": 3,
        },
    ]

    # In test environments we want to avoid real charges, so we override the
    # prices to a symbolic 1 MXN while keeping real prices for main/staging.
    env = getattr(settings, "ALTIQ_ENV", "main") or "main"
    env_normalized = env.strip().lower()
    if env_normalized in {"test", "testing"}:
        for data in packages:
            data["price_mxn"] = Decimal("1")

    for data in packages:
        slug = data.pop("slug")
        ServicePackage.objects.update_or_create(slug=slug, defaults=data)

