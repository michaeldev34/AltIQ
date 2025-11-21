from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import CustomQuoteRequest, MeetingRequest


def contact(request):
    if request.method == "POST":
        form_type = request.POST.get("type")
        if form_type == "quote":
            CustomQuoteRequest.objects.create(
                full_name=request.POST.get("full_name", "").strip(),
                company_name=request.POST.get("company_name", "").strip(),
                email=request.POST.get("email", "").strip(),
                phone=request.POST.get("phone", "").strip(),
                industry=request.POST.get("industry", "").strip(),
                location=request.POST.get("location", "").strip(),
                current_challenge=request.POST.get("current_challenge", "").strip(),
                desired_outcome=request.POST.get("desired_outcome", "").strip(),
            )
            messages.success(request, "Gracias, preparamos una cotizaci3n con base en tu informaci3n.")
        elif form_type == "meeting":
            MeetingRequest.objects.create(
                full_name=request.POST.get("full_name", "").strip(),
                company_name=request.POST.get("company_name", "").strip(),
                email=request.POST.get("email", "").strip(),
                phone=request.POST.get("phone", "").strip(),
                meeting_type=request.POST.get("meeting_type", "remote"),
                preferred_date=request.POST.get("preferred_date") or None,
                preferred_time_range=request.POST.get("preferred_time_range", "").strip(),
                notes=request.POST.get("notes", "").strip(),
            )
            messages.success(request, "Gracias, revisaremos tu solicitud de reuni3n y te contactaremos.")
        return redirect("contact")

    return render(request, "contacts/contact.html")

