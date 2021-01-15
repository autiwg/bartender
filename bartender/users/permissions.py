from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": "authenticated",
            "effect": "allow",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)


class TransactionAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": "authenticated",
            "effect": "allow",
        }
    ]

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
