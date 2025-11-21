from __future__ import annotations

from django.shortcuts import render

from .models import CaseStudy


def case_list(request):
    cases = CaseStudy.objects.all().order_by("-is_featured", "-created_at")
    return render(request, "cases/list.html", {"cases": cases})

