from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bartender.users.exceptions import InvalidInviteError
from bartender.users.permissions import (
    UserAccessPolicy,
    TransactionAccessPolicy,
    InviteAccessPolicy,
)
from bartender.users.serializers import (
    UserSerializer,
    TransactionSerializer,
    InviteSerializer,
    UserInviteSignupSerializer,
)
from bartender.users.models import User, Transaction, Invite
from bartender.view_mixins import AccessPolicyMixin


class UserViewSet(AccessPolicyMixin, ModelViewSet):
    queryset = User.objects.order_by("pk")
    serializer_class = UserSerializer
    permission_classes = (UserAccessPolicy,)

    @action(methods=["post"], detail=False)
    def accept_invite(self, request):
        serializer = UserInviteSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


class TransactionViewSet(AccessPolicyMixin, ModelViewSet):
    queryset = Transaction.objects.order_by("pk")
    serializer_class = TransactionSerializer
    permission_classes = (TransactionAccessPolicy,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class InviteViewSet(AccessPolicyMixin, ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = (InviteAccessPolicy,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)
