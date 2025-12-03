from django.db import migrations


def create_default_packages(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    packages = [
        {"slug": "basic", "name_es": "Paquete Básico", "name_en": "Basic Package",
         "short_description_es": "Reportes puntuales sobre tu operación.",
         "price_mxn": "500", "is_active": True, "display_order": 1},
        {"slug": "medium", "name_es": "Paquete Medium", "name_en": "Medium Package",
         "short_description_es": "Diagnóstico profundo y recomendaciones.",
         "price_mxn": "3000", "is_active": True, "display_order": 2},
        {"slug": "master", "name_es": "Paquete Master", "name_en": "Master Package",
         "short_description_es": "Solución digital hecha a la medida.",
         "price_mxn": "15000", "is_active": True, "display_order": 3},
    ]
    for pkg in packages:
        ServicePackage.objects.update_or_create(slug=pkg.pop("slug"), defaults=pkg)


class Migration(migrations.Migration):
    dependencies = [("services", "0001_initial")]
    operations = [migrations.RunPython(create_default_packages, migrations.RunPython.noop)]

