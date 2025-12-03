from __future__ import annotations

from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
	    # Temporary cart endpoint: currently just redirects into checkout.
	    # Later we can implement a real session-based cart using this route.
	    path("cart/add/<slug:package_slug>/", views.cart_add, name="cart_add"),

	    # Dedicated status endpoints must come *before* the catch-all slug pattern,
	    # otherwise "success" / "failure" would be treated as package slugs.
	    path("success/", views.checkout_success, name="success"),
	    path("failure/", views.checkout_failure, name="failure"),

	    # /checkout/<package_slug>/
	    path("<slug:package_slug>/", views.checkout, name="checkout"),
	]

