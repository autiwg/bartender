from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework.serializers import ModelSerializer

from bartender.users.models import User, Transaction, Invite
from bartender.util import map_kwargs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("groups", "password", "user_permissions", "transactions")


class TransactionSerializer(ModelSerializer):
    amount_total = MoneyField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Transaction
        fields = ("id", "user", "crate", "amount", "amount_total")
        extra_kwargs = map_kwargs("user", read_only=True)


class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = ("id", "created_at", "created_by", "token", "is_valid")
        extra_kwargs = map_kwargs("token", "created_by", "is_valid", read_only=True)
