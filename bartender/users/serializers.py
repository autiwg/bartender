import requests
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from bartender import settings
from bartender.users.models import User, Transaction, Invite
from bartender.util import map_kwargs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("groups", "password", "user_permissions", "transactions")


class UserInviteSignupSerializer(serializers.ModelSerializer):
    invite = serializers.CharField(max_length=8, min_length=8)
    telegram_id = serializers.IntegerField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with specified Telegram Chat ID already exists",
            ),
        ],
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self._telegram_user = None
        super(UserInviteSignupSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("invite", "telegram_id")
        extra_kwargs = map_kwargs("telegram_id", "invite", required=True)

    def validate_invite(self, value):
        qs = Invite.objects.filter(token=value, invited_user__isnull=True)
        if not qs.exists():
            raise serializers.ValidationError("No such invite found")
        return value

    def validate_telegram_id(self, value):
        self._telegram_user = User.get_telegram_chat(value)
        if self._telegram_user is None:
            raise serializers.ValidationError("Telegram returned empty user data")
        return value

    def create(self, validated_data):
        token = validated_data.pop("invite")
        invite = Invite.objects.get(token=token)
        validated_data["username"] = validated_data.get("telegram_id")
        validated_data["first_name"] = self._telegram_user["first_name"]
        validated_data["last_name"] = self._telegram_user["last_name"]
        user = super(UserInviteSignupSerializer, self).create(validated_data)
        user.invite = invite
        user.save()
        return user


class TransactionSerializer(serializers.ModelSerializer):
    amount_total = MoneyField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Transaction
        fields = ("id", "user", "crate", "amount", "amount_total")
        extra_kwargs = map_kwargs("user", read_only=True)


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ("id", "created_at", "created_by", "token", "is_valid")
        extra_kwargs = map_kwargs("token", "created_by", "is_valid", read_only=True)
