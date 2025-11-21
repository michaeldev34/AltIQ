from __future__ import annotations

from django.shortcuts import render

from .models import ServicePackage


def service_list(request):
    packages = ServicePackage.objects.filter(is_active=True).order_by("display_order", "id")
    return render(request, "services/list.html", {"packages": packages})

