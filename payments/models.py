from __future__ import annotations

from django.db import models

from orders.models import Order


class Payment(models.Model):
    """Represents a payment attempt or completed payment for an Order."""

    METHOD_CHOICES = [
        ("paypal", "PayPal"),
        ("coinbase", "Coinbase Commerce"),
    ]

    STATUS_CHOICES = [
        ("created", "Created"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")

    # External gateway identifiers
    provider_payment_id = models.CharField(max_length=120, blank=True)
    provider_session_id = models.CharField(max_length=120, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="MXN")

    raw_payload = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Payment #{self.pk} ({self.method}) - {self.status}"

