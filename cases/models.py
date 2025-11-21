from __future__ import annotations

from django.db import models


class CaseStudy(models.Model):
    """Industrial case study summarizing problem, solution and impact."""

    slug = models.SlugField(unique=True)
    title_es = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)

    industry = models.CharField(max_length=150, blank=True)

    problem_es = models.TextField()
    problem_en = models.TextField(blank=True)

    solution_es = models.TextField()
    solution_en = models.TextField(blank=True)

    impact_es = models.TextField(help_text="Resultados concretos, ej. -15% paros no programados")
    impact_en = models.TextField(blank=True)

    highlight_metric = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return self.title_es

