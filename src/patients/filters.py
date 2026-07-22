from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

if TYPE_CHECKING:
    from patients.models import Patient


ALLOWED_ORDERING_FIELDS: dict[str, str] = {
    "last_name": "last_name",
    "created_at": "created_at",
    "last_appointment": "last_appointment_date",
}


class PatientFilter:
    """ Stateless filter that narrows a Patient queryset from query params.

        Handles search (multi-field icontains) and ordering (whitelisted fields).
    """

    def __init__(self, query_params: dict[str, str]) -> None:
        self.query_params = query_params

    def filter_queryset(self, queryset: QuerySet["Patient"]) -> QuerySet["Patient"]:
        queryset = self._apply_search(queryset)
        queryset = self._apply_ordering(queryset)
        return queryset

    def _apply_search(self, queryset: QuerySet["Patient"]) -> QuerySet["Patient"]:
        search = self.query_params.get("search", "").strip()
        if not search:
            return queryset

        return queryset.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(dni__icontains=search)
        )

    def _apply_ordering(self, queryset: QuerySet["Patient"]) -> QuerySet["Patient"]:
        ordering = self.query_params.get("ordering", "").strip()
        if not ordering:
            return queryset.order_by("last_name")

        descending = ordering.startswith("-")
        field = ordering.lstrip("-")

        if field not in ALLOWED_ORDERING_FIELDS:
            return queryset.order_by("last_name")

        resolved = ALLOWED_ORDERING_FIELDS[field]
        if descending:
            resolved = f"-{resolved}"

        return queryset.order_by(resolved)
