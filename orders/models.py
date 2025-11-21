from __future__ import annotations

from django.conf import settings
from django.db import models

from services.models import ServicePackage


class Order(models.Model):
    """Represents a purchase intent for a ServicePackage.

    User data is kept minimal for now; later we can connect to an authenticated user
    model or a separate CRM.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    package = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name="orders")

    # Basic contact / billing fields (Spanish labels handled at form/template level).
    customer_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=180, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    # For now store MXN as numeric + currency code.
    currency = models.CharField(max_length=10, default="MXN")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Optional link to an authenticated user if we ever enable login.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="altiq_orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Order #{self.pk} - {self.package} - {self.status}"

