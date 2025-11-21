from __future__ import annotations

from django.db import models


class ServicePackage(models.Model):
    """Productized AltIQ service package purchasable online.

    Three main packages will be created via fixtures or the admin:
    - Diagnóstico Rápido
    - Piloto en Planta
    - Acompañamiento Continuo
    """

    slug = models.SlugField(unique=True, help_text="URL-safe identifier, e.g. diagnostico-rapido")

    # Spanish-first, with optional English fields for later localization.
    name_es = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120, blank=True)

    short_description_es = models.CharField(max_length=255)
    short_description_en = models.CharField(max_length=255, blank=True)

    # Longer marketing copy (can be used on detail/checkout pages).
    description_es = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    # Pricing in MXN for now; can be extended with multi-currency later.
    price_mxn = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name_es or self.slug

