from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from bartender.users.exceptions import InvalidTelegramIDError
from bartender.users.models import User, Transaction, Invite
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
    queryset = Transaction.objects.order_by("-created_at")
    serializer_class = TransactionSerializer
    permission_classes = (TransactionAccessPolicy,)
    filter_fields = ("id", "user", "crate", "amount")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["post"], detail=True)
    def increment(self, request, pk=None):
        transaction = get_object_or_404(Transaction, id=pk)
        transaction.amount += 1
        transaction.save()
        return redirect(reverse("transaction-detail", [pk]))


class InviteViewSet(AccessPolicyMixin, ModelViewSet):
    queryset = Invite.objects.order_by("-created_at")
    serializer_class = InviteSerializer
    permission_classes = (InviteAccessPolicy,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(["post"])
@permission_classes([AllowAny])
def retrieve_token(request):
    telegram_chat_id = request.data.get("telegram_id")
    if telegram_chat_id is None:
        raise InvalidTelegramIDError("No telegram_id provided")
    try:
        user = User.objects.get(telegram_id=telegram_chat_id)
    except User.DoesNotExist:
        raise InvalidTelegramIDError
    if user.revalidate_telegram_id() is False:
        user.delete()
        raise InvalidTelegramIDError(
            detail="Telegram returned invalid chat data, user delted",
            code="invalid_user",
        )
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
