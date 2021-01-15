from rest_framework.decorators import action
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
)
from bartender.users.models import User, Transaction, Invite
from bartender.view_mixins import AccessPolicyMixin


class UserViewSet(AccessPolicyMixin, ModelViewSet):
    queryset = User.objects.order_by("pk")
    serializer_class = UserSerializer
    permission_classes = (UserAccessPolicy,)

    @action(methods=["post"], detail=False)
    def accept_invite(self, request):
        invite_token = request.data.pop("invite")
        try:
            invite = Invite.objects.get(
                invite_token=invite_token,
            )
            assert invite.is_valid
        except Invite.DoesNotExist:
            raise InvalidInviteError("Provided invite code is invalid")
        except AssertionError:
            raise InvalidInviteError("Provided invite code has already been used")


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
