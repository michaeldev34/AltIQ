from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from services.models import ServicePackage
from payments.models import Payment
from payments.utils import (
    PaymentGatewayError,
    create_coinbase_charge,
    create_paypal_order,
)
from .models import Order

@login_required
def checkout(request: HttpRequest, package_slug: str) -> HttpResponse:
    """Create an Order + Payment and redirect to PayPal or Coinbase.

    If gateway configuration is missing or an error occurs, the user is sent to
    the generic failure page.
    """

    package = get_object_or_404(ServicePackage, slug=package_slug, is_active=True)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        company_name = request.POST.get("company_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        payment_method = request.POST.get("payment_method", "paypal")

        if customer_name and email:
            order = Order.objects.create(
                package=package,
                customer_name=customer_name,
                company_name=company_name,
                email=email,
                phone=phone,
                currency="MXN",
                amount=package.price_mxn,
                status="pending",
                user=request.user if request.user.is_authenticated else None,
            )

            payment = Payment.objects.create(
                order=order,
                method="coinbase" if payment_method == "coinbase" else "paypal",
                amount=order.amount,
                currency=order.currency,
                status="created",
            )

            success_url = request.build_absolute_uri(reverse("orders:success"))
            cancel_url = request.build_absolute_uri(reverse("orders:failure"))

            try:
                if payment.method == "paypal":
                    approval_url, provider_id = create_paypal_order(order, success_url, cancel_url)
                else:
                    approval_url, provider_id = create_coinbase_charge(order, success_url, cancel_url)
            except PaymentGatewayError:
                payment.status = "failed"
                payment.save(update_fields=["status"])
                order.status = "failed"
                order.save(update_fields=["status"])
                return redirect("orders:failure")

            payment.provider_payment_id = provider_id
            payment.status = "pending"
            payment.save(update_fields=["provider_payment_id", "status"])

            return redirect(approval_url)

    context = {"package": package}
    return render(request, "orders/checkout.html", context)

@login_required
def cart_add(request: HttpRequest, package_slug: str) -> HttpResponse:
    """Temporary placeholder for a real cart.

    For now, "Anadir al carrito" behaves like "Comprar ahora" and simply
    redirects into the single-package checkout flow. This keeps templates and
    tests working while we gradually introduce a proper multi-item cart.
    """

    return redirect("orders:checkout", package_slug=package_slug)


def checkout_success(request: HttpRequest) -> HttpResponse:
    """Thank-you page after a successful payment.

    We show the most recent completed order if available; the page still
    renders without it so it works even if a user refreshes later.
    """

    order = (
        Order.objects.filter(status="paid")
        .order_by("-created_at")
        .select_related("package")
        .first()
    )
    return render(request, "orders/success.html", {"order": order})



def checkout_failure(request: HttpRequest) -> HttpResponse:
    """Simple error page when a payment cannot be completed."""
    return render(request, "orders/failure.html")
