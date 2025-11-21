from __future__ import annotations

import json

from django.test import TestCase
from django.urls import reverse

from orders.models import Order
from payments.models import Payment
from services.models import ServicePackage


class PaypalWebhookTests(TestCase):
    def setUp(self) -> None:
        package = ServicePackage.objects.create(
            slug="webhook-test",
            name_es="Paquete webhook",
            name_en="Webhook package",
            short_description_es="",
            short_description_en="",
            description_es="",
            description_en="",
            price_mxn=100,
            is_active=True,
            display_order=1,
        )
        self.order = Order.objects.create(
            package=package,
            customer_name="Test User",
            company_name="AltIQ Test",
            email="test@example.com",
            phone="",
            currency="MXN",
            amount=100,
            status="pending",
        )
        self.payment = Payment.objects.create(
            order=self.order,
            method="paypal",
            amount=self.order.amount,
            currency=self.order.currency,
            status="created",
            provider_payment_id="PAYPAL-123",
        )

    def test_paypal_webhook_marks_payment_and_order_paid(self) -> None:
        url = reverse("payments:paypal_webhook")
        payload = {
            "resource": {"id": "PAYPAL-123"},
        }
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.payment.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(self.payment.status, "completed")
        self.assertEqual(self.order.status, "paid")


class CoinbaseWebhookTests(TestCase):
    def setUp(self) -> None:
        package = ServicePackage.objects.create(
            slug="webhook-test-coinbase",
            name_es="Paquete webhook Coinbase",
            name_en="Webhook package Coinbase",
            short_description_es="",
            short_description_en="",
            description_es="",
            description_en="",
            price_mxn=100,
            is_active=True,
            display_order=1,
        )
        self.order = Order.objects.create(
            package=package,
            customer_name="Test User",
            company_name="AltIQ Test",
            email="test@example.com",
            phone="",
            currency="MXN",
            amount=100,
            status="pending",
        )
        self.payment = Payment.objects.create(
            order=self.order,
            method="coinbase",
            amount=self.order.amount,
            currency=self.order.currency,
            status="created",
            provider_payment_id="COINBASE-123",
        )

    def test_coinbase_webhook_marks_payment_and_order_paid(self) -> None:
        url = reverse("payments:coinbase_webhook")
        payload = {
            "type": "charge:confirmed",
            "data": {
                "id": "COINBASE-123",
                "timeline": [{"status": "NEW"}, {"status": "COMPLETED"}],
            },
        }
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.payment.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(self.payment.status, "completed")
        self.assertEqual(self.order.status, "paid")

