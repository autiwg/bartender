class AccessPolicyMixin:
    """
    Mixin to provide access_policy and automatic override of get_queryset()
    """

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, self.queryset)
