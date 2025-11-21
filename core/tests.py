from __future__ import annotations

from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_home_page_renders(self) -> None:
        """The main landing page at `/` should render with HTTP 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AltIQ")

