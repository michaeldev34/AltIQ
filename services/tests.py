from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from .models import ServicePackage


class ServiceViewsTests(TestCase):
    def setUp(self) -> None:
        self.package = ServicePackage.objects.create(
            slug="pilot-line-mx",
            name_es="Linea piloto",
            name_en="Pilot line",
            short_description_es="Prueba controlada en planta.",
            short_description_en="Controlled pilot in plant.",
            description_es="",
            description_en="",
            price_mxn=10000,
            is_active=True,
            display_order=1,
        )

    def test_service_list_renders(self) -> None:
        url = reverse("services:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.package.name_es)

