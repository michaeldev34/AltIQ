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

    # Track whether we already sent the thank-you email with access codes
    thank_you_email_sent = models.BooleanField(default=False)

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


class OrderItem(models.Model):
    """Individual line item within an Order.

    This lets a single order contain multiple service packages with quantities.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    package = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Item x{self.quantity} - {self.package} (order {self.order_id})"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class OrderCode(models.Model):
    """Stores a generated code per order and product category.

    There should be at most one code per (order, package) pair.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="codes")
    package = models.ForeignKey(ServicePackage, on_delete=models.PROTECT, related_name="order_codes")
    code = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("order", "package")
        ordering = ["id"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Code {self.code} for {self.package} (order {self.order_id})"

