from __future__ import annotations

from decimal import Decimal

from django.db import migrations


BASIC_SLUG = "basic"
MEDIUM_SLUG = "medium"
MASTER_SLUG = "master"


def create_default_packages(apps, schema_editor):  # noqa: ARG001
    ServicePackage = apps.get_model("services", "ServicePackage")

    packages = [
        {
            "slug": BASIC_SLUG,
            "name_es": "Paquete Básico",
            "name_en": "Basic Package",
            "short_description_es": "Reportes puntuales sobre tu operación y datos clave.",
            "short_description_en": "Focused reports on your operation and key data.",
            "description_es": "Primer acercamiento para entender tu línea, capturar datos y detectar oportunidades inmediatas sin fricción.",
            "description_en": "Initial engagement to understand your line, capture data and detect quick-win opportunities.",
            "price_mxn": Decimal("500"),
            "is_active": True,
            "display_order": 1,
        },
        {
            "slug": MEDIUM_SLUG,
            "name_es": "Paquete Medium",
            "name_en": "Medium Package",
            "short_description_es": "Diagnóstico profundo y recomendaciones priorizadas.",
            "short_description_en": "Deeper diagnostic and prioritized recommendations.",
            "description_es": "Analizamos variabilidad, cuellos de botella y escenarios financieros para reducir desperdicio y mejorar flujo.",
            "description_en": "We analyze variability, bottlenecks and financial scenarios to reduce waste and improve flow.",
            "price_mxn": Decimal("3000"),
            "is_active": True,
            "display_order": 2,
        },
        {
            "slug": MASTER_SLUG,
            "name_es": "Paquete Master",
            "name_en": "Master Package",
            "short_description_es": "Implementación de una solución digital hecha a la medida.",
            "short_description_en": "Implementation of a custom digital solution.",
            "description_es": "Incluye el diagnóstico Medium más el desarrollo de un producto web enfocado en un problema específico de tu planta.",
            "description_en": "Includes the Medium diagnostic plus a web product focused on a specific problem in your plant.",
            "price_mxn": Decimal("15000"),
            "is_active": True,
            "display_order": 3,
        },
    ]

    for data in packages:
        slug = data.pop("slug")
        ServicePackage.objects.update_or_create(slug=slug, defaults=data)


def delete_default_packages(apps, schema_editor):  # noqa: ARG001
    ServicePackage = apps.get_model("services", "ServicePackage")
    ServicePackage.objects.filter(slug__in=[BASIC_SLUG, MEDIUM_SLUG, MASTER_SLUG]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_packages, delete_default_packages),
    ]

