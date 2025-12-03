from __future__ import annotations

from django.shortcuts import render

from .defaults import ensure_default_individual_services, ensure_default_service_packages
from .models import IndividualService, ServicePackage


def service_list(request):
    # Make sure both individual services and packages exist
    ensure_default_individual_services()
    ensure_default_service_packages()

    individual_services = IndividualService.objects.filter(is_active=True).order_by("display_order", "id")
    packages = ServicePackage.objects.filter(is_active=True).order_by("display_order", "id")

    return render(request, "services/list.html", {
        "individual_services": individual_services,
        "packages": packages,
    })

