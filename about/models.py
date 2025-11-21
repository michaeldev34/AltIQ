from __future__ import annotations

from django.db import models


class Expert(models.Model):
    """AltIQ expert profile for the About page."""

    full_name = models.CharField(max_length=150)
    role_es = models.CharField(max_length=150)
    role_en = models.CharField(max_length=150, blank=True)

    bio_es = models.TextField()
    bio_en = models.TextField(blank=True)

    # Optional avatar URL or path; real file handling can be added later.
    avatar_url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)

    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:  # pragma: no cover
        return self.full_name

