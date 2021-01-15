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
            "action": WRITE_ACTIONS,
            "principal": "authenticated",
            "effect": "allow",
            "condition": "user_must_be:is_staff",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_staff:
            return qs
        return qs.filter(billed=False)
