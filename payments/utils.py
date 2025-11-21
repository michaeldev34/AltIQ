from __future__ import annotations

"""Helpers for talking to PayPal and Coinbase Commerce without extra deps.

These functions use the Python stdlib (urllib) so we do not need to install
additional HTTP client libraries. They are intentionally minimal and suitable
for a first MVP; hardening (signature verification, retries, logging) can be
added later.
"""

import base64
import json
import os
from decimal import Decimal
from typing import TYPE_CHECKING, Tuple

import urllib.error
import urllib.request

if TYPE_CHECKING:  # pragma: no cover - import only for type checkers
    from orders.models import Order


class PaymentGatewayError(Exception):
    """Raised when a call to an external payment gateway fails."""


def _to_str_amount(value: Decimal | float | int) -> str:
    """Convert a numeric value to a plain string acceptable by gateways."""

    return format(Decimal(value), "f")


# ---------------------------------------------------------------------------
# PayPal helpers
# ---------------------------------------------------------------------------


def _paypal_base_url() -> str:
    env = os.getenv("PAYPAL_ENV", "sandbox").lower()
    if env == "live":
        return "https://api-m.paypal.com"
    return "https://api-m.sandbox.paypal.com"


def create_paypal_order(order: "Order", success_url: str, cancel_url: str) -> Tuple[str, str]:
    """Create a PayPal order and return (approval_url, paypal_order_id).

    Environment variables required:
      - PAYPAL_CLIENT_ID
      - PAYPAL_CLIENT_SECRET
      - optional PAYPAL_ENV ("sandbox" or "live")
    """

    client_id = os.getenv("PAYPAL_CLIENT_ID")
    secret = os.getenv("PAYPAL_CLIENT_SECRET")
    if not client_id or not secret:
        raise PaymentGatewayError("PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET not configured")

    auth = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    base = _paypal_base_url()

    # 1) Obtain access token
    token_req = urllib.request.Request(
        f"{base}/v1/oauth2/token",
        data="grant_type=client_credentials".encode(),
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(token_req, timeout=10) as resp:
            token_data = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        raise PaymentGatewayError(f"PayPal token error: {exc}") from exc

    access_token = token_data.get("access_token")
    if not access_token:
        raise PaymentGatewayError("PayPal access token missing from response")

    # 2) Create order
    body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": order.currency or "MXN",
                    "value": _to_str_amount(order.amount),
                },
                "custom_id": str(order.id),
            }
        ],
        "application_context": {
            "return_url": success_url,
            "cancel_url": cancel_url,
        },
    }

    order_req = urllib.request.Request(
        f"{base}/v2/checkout/orders",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(order_req, timeout=10) as resp:
            order_data = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        raise PaymentGatewayError(f"PayPal order error: {exc}") from exc

    approval_url = None
    for link in order_data.get("links", []):
        if link.get("rel") == "approve":
            approval_url = link.get("href")
            break

    if not approval_url:
        raise PaymentGatewayError("PayPal approval URL not found in response")

    return approval_url, order_data.get("id", "")


# ---------------------------------------------------------------------------
# Coinbase Commerce helpers
# ---------------------------------------------------------------------------


def create_coinbase_charge(order: "Order", success_url: str, cancel_url: str) -> Tuple[str, str]:
    """Create a Coinbase Commerce charge and return (hosted_url, charge_id).

    Environment variables required:
      - COINBASE_COMMERCE_API_KEY
    """

    api_key = os.getenv("COINBASE_COMMERCE_API_KEY")
    if not api_key:
        raise PaymentGatewayError("COINBASE_COMMERCE_API_KEY not configured")

    body = {
        "name": order.package.name_es,
        "description": order.package.short_description_es,
        "pricing_type": "fixed_price",
        "local_price": {
            "amount": _to_str_amount(order.amount),
            "currency": order.currency or "MXN",
        },
        "metadata": {"order_id": order.id},
        "redirect_url": success_url,
        "cancel_url": cancel_url,
    }

    req = urllib.request.Request(
        "https://api.commerce.coinbase.com/charges",
        data=json.dumps(body).encode(),
        headers={
            "X-CC-Api-Key": api_key,
            "X-CC-Version": "2018-03-22",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        raise PaymentGatewayError(f"Coinbase charge error: {exc}") from exc

    charge = data.get("data", {})
    hosted_url = charge.get("hosted_url")
    charge_id = charge.get("id", "")

    if not hosted_url:
        raise PaymentGatewayError("Coinbase hosted_url not found in response")

    return hosted_url, charge_id

