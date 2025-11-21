from __future__ import annotations

from unittest import mock

from django.test import TestCase
from django.urls import reverse

from services.models import ServicePackage
from .models import Order
from payments.models import Payment
from payments.utils import PaymentGatewayError


class CheckoutFlowTests(TestCase):
    def setUp(self) -> None:
        self.package = ServicePackage.objects.create(
            slug="pilot-line-mx",
            name_es="Linea piloto",
            name_en="Pilot line",
            short_description_es="Prueba controlada en planta.",
            short_description_en="Controlled pilot in plant.",
            description_es="",
            description_en="",
            price_mxn=15000,
            is_active=True,
            display_order=1,
        )

    @mock.patch("orders.views.create_paypal_order")
    def test_checkout_creates_order_and_payment_and_redirects(self, mock_create_paypal):
        mock_create_paypal.return_value = ("https://paypal.test/approve", "PAYPAL-ID-123")

        url = reverse("orders:checkout", kwargs={"package_slug": self.package.slug})
        payload = {
            "customer_name": "Test User",
            "company_name": "AltIQ Test",
            "email": "test@example.com",
            "phone": "+52 55 0000 0000",
            "payment_method": "paypal",
        }

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://paypal.test/approve")

        order = Order.objects.get()
        payment = Payment.objects.get()

        self.assertEqual(order.package, self.package)
        self.assertEqual(order.status, "pending")
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.method, "paypal")
        self.assertEqual(payment.status, "pending")
        self.assertEqual(payment.provider_payment_id, "PAYPAL-ID-123")

    @mock.patch("orders.views.create_paypal_order", side_effect=PaymentGatewayError("gateway error"))
    def test_checkout_gateway_error_sends_to_failure(self, _mock_create_paypal):
        url = reverse("orders:checkout", kwargs={"package_slug": self.package.slug})
        payload = {
            "customer_name": "Test User",
            "company_name": "AltIQ Test",
            "email": "test@example.com",
            "phone": "+52 55 0000 0000",
            "payment_method": "paypal",
        }

        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("orders:failure"))

        order = Order.objects.get()
        payment = Payment.objects.get()
        self.assertEqual(order.status, "failed")
        self.assertEqual(payment.status, "failed")

