from __future__ import annotations
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation(order):
    """Send order confirmation email to customer."""
    subject = f"AltIQ - Confirmación de pedido #{order.id}"
    message = render_to_string("emails/order_thank_you.txt", {"order": order})
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@altiq.mx',
        [order.email],
        fail_silently=True,
    )


def send_order_thank_you_email_with_codes(order):
    """Send order confirmation with service codes."""
    send_order_confirmation(order)

