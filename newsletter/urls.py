from __future__ import annotations

from django.urls import path

from . import views

app_name = "newsletter"


urlpatterns = [
    path("", views.article_list, name="list"),
]
