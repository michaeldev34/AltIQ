from __future__ import annotations

from django.db import models


class CustomQuoteRequest(models.Model):
    """Request for a tailored proposal from AltIQ."""

    full_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=180, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    # High-level context fields tailored to industrial Mexico context.
    industry = models.CharField(max_length=150, blank=True, help_text="Ej. ferretera, petroqumica, logstica")
    location = models.CharField(max_length=150, blank=True)

    current_challenge = models.TextField(help_text="Describe el problema principal que quieres resolver")
    desired_outcome = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Custom quote - {self.company_name or self.full_name}"


class MeetingRequest(models.Model):
    """In-person or remote consultation request."""

    MEETING_TYPE_CHOICES = [
        ("remote", "Remota"),
        ("on_site", "En sitio"),
    ]

    full_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=180, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES, default="remote")
    preferred_date = models.DateField(blank=True, null=True)
    preferred_time_range = models.CharField(max_length=120, blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Meeting - {self.company_name or self.full_name} ({self.meeting_type})"

