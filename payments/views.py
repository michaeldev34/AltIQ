from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Payment


@csrf_exempt
@require_POST
def paypal_webhook(request: HttpRequest) -> HttpResponse:
    """Very small PayPal webhook handler for MVP.

    For now we trust PayPal's call (IPN/webhook) and only look at the
    order/payment identifiers. Proper signature verification can be added
    before going live.
    """

    data = request.body.decode() or "{}"
    try:
        payload = json.loads(data)
    except Exception:  # pragma: no cover - defensive, we just ignore bad JSON
        return HttpResponse(status=400)

    resource = payload.get("resource", {})
    paypal_order_id = resource.get("id") or resource.get("supplementary_data", {}).get("related_ids", {}).get("order_id")

    if not paypal_order_id:
        return HttpResponse(status=400)

    payment = Payment.objects.filter(provider_payment_id=paypal_order_id, method="paypal").select_related("order").first()
    if not payment:
        return HttpResponse(status=200)

    payment.status = "completed"
    payment.raw_payload = payload
    payment.save(update_fields=["status", "raw_payload"])

    payment.order.status = "paid"
    payment.order.save(update_fields=["status"])

    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_POST
def coinbase_webhook(request: HttpRequest) -> HttpResponse:
    """Very small Coinbase Commerce webhook handler for MVP.

    We simply trust the event for now and mark the payment as completed when
    the charge is marked "CONFIRMED". Signature verification is intentionally
    left for a later hardening pass.
    """

    data = request.body.decode() or "{}"
    try:
        payload = json.loads(data)
    except Exception:  # pragma: no cover
        return HttpResponse(status=400)

    event_type = payload.get("type")
    charge = payload.get("data", {})
    charge_id = charge.get("id")
    timeline = charge.get("timeline", [])

    if not charge_id:
        return HttpResponse(status=400)

    last_status = None
    if timeline:
        last_status = timeline[-1].get("status")

    payment = Payment.objects.filter(provider_payment_id=charge_id, method="coinbase").select_related("order").first()
    if not payment:
        return HttpResponse(status=200)

    if event_type == "charge:confirmed" or last_status == "COMPLETED":
        payment.status = "completed"
        payment.order.status = "paid"
        order_update_fields = ["status"]
    elif event_type in {"charge:failed", "charge:expired"} or last_status in {"FAILED", "EXPIRED"}:
        payment.status = "failed"
        payment.order.status = "failed"
        order_update_fields = ["status"]
    else:
        # Other statuses are ignored for now but payload is stored.
        payment.raw_payload = payload
        payment.save(update_fields=["raw_payload"])
        return JsonResponse({"status": "ignored"})

    payment.raw_payload = payload
    payment.save(update_fields=["status", "raw_payload"])
    payment.order.save(update_fields=order_update_fields)

    return JsonResponse({"status": "ok"})

