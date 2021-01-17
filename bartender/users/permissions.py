from django.utils import timezone
from rest_access_policy import AccessPolicy

from bartender.permissions import WRITE_ACTIONS


class UserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": "authenticated",
            "effect": "allow",
        },
        {"action": "accept_invite", "principal": "*", "effect": "allow"},
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)


class TransactionAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>", "create", "destroy"],
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ["update", "partial_update", "increment"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "transaction_is_today",
        },
    ]

    def transaction_is_today(self, request, view, action) -> bool:
        transaction = view.get_object()
        return transaction.created_at.date() == timezone.now().date()

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs.filter(user=request.user)


class InviteAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": "authenticated",
            "effect": "allow",
            "condition": "user_must_be:is_staff",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        return qs
