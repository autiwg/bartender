from django.db.models import Count
from rest_access_policy import AccessPolicy

from bartender.permissions import WRITE_ACTIONS


class CrateAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>", "consumption"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": [WRITE_ACTIONS, "bill", "balance"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "user_must_be:is_staff",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_staff:
            return qs
        return (
            qs.annotate(amount_sum_transactions=Count("transactions"))
            .filter(billed=False)
            .order_by("-amount_sum_transactions")
        )
