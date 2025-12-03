from __future__ import annotations

import secrets
from typing import Iterable, List

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string

from services.models import ServicePackage
from .models import Order, OrderCode


_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def _random_block(length: int = 4) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def generate_code_for_package(package: ServicePackage) -> str:
    """Generate a code whose pattern depends on the package category.

    - Basic-like packages -> prefix BSC
    - Medium-like packages -> prefix MED
    - Master-like packages -> prefix MST
    - Fallback -> prefix ALT
    """

    slug = (package.slug or "").lower()
    if "basic" in slug or "basico" in slug:
        prefix = "BSC"
    elif "medium" in slug or "medio" in slug:
        prefix = "MED"
    elif "master" in slug:
        prefix = "MST"
    else:
        prefix = "ALT"

    # Vary the pattern slightly by category to make them feel different.
    if prefix == "BSC":
        return f"{prefix}-{_random_block(4)}-{_random_block(4)}"
    if prefix == "MED":
        return f"{prefix}-{_random_block(5)}-{_random_block(3)}"
    if prefix == "MST":
        return f"{prefix}-{_random_block(4)}-{_random_block(4)}-{_random_block(2)}"
    return f"{prefix}-{_random_block(4)}-{_random_block(4)}"


def _unique_packages_for_order(order: Order) -> List[ServicePackage]:
    """Return distinct ServicePackage instances involved in the order."""

    packages: list[ServicePackage] = []
    seen_ids: set[int] = set()

    items_qs = order.items.select_related("package")
    if items_qs.exists():
        for item in items_qs:
            if item.package_id and item.package_id not in seen_ids:
                packages.append(item.package)
                seen_ids.add(item.package_id)
    elif order.package_id:
        packages.append(order.package)

    return packages


def send_order_thank_you_email_with_codes(order: Order) -> None:
    """Generate one code per product category and send a single email.

    Safe to call multiple times: it is idempotent and will only send once.
    """

    if not order.email:
        return

    with transaction.atomic():
        order = Order.objects.select_for_update().select_related("package").get(pk=order.pk)
        if order.thank_you_email_sent:
            return

        packages = _unique_packages_for_order(order)
        codes: list[OrderCode] = []
        for package in packages:
            code_obj, _created = OrderCode.objects.get_or_create(
                order=order,
                package=package,
                defaults={"code": generate_code_for_package(package)},
            )
            codes.append(code_obj)

        # If for some reason there are no packages, mark as sent to avoid loops.
        if not codes:
            order.thank_you_email_sent = True
            order.save(update_fields=["thank_you_email_sent"])
            return

        subject = "Confirmacion de pago - AltIQ"
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@altiq.mx")

        context = {
            "order": order,
            "codes": codes,
        }
        body = render_to_string("emails/order_thank_you.txt", context).strip()

        send_mail(subject, body, from_email, [order.email])

        order.thank_you_email_sent = True
        order.save(update_fields=["thank_you_email_sent"])

