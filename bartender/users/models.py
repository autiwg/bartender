from django.contrib.auth.models import AbstractUser
from django.db import models

from bartender.drinks.models import Crate
from bartender.mixins import BaseModel
from bartender.users.generators import generate_invite_token


class Invite(BaseModel):
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_invites",
    )
    token = models.CharField(
        max_length=4, default=generate_invite_token, editable=False, unique=True
    )

    @property
    def is_valid(self):
        return not self.invited_user.exists()


class User(AbstractUser):
    telegram_id = models.BigIntegerField(
        help_text="Telegram User ID", editable=False, null=True, unique=True
    )
    invite = models.ForeignKey(
        Invite, null=True, on_delete=models.SET_NULL, related_name="invited_user"
    )
    transactions = models.ManyToManyField(
        to=Crate, related_name="transactions", through="Transaction"
    )


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="Amount of bottles purchased")

    @property
    def amount_total(self):
        return self.amount * self.crate.bottle_price

    def __str__(self):
        return "%s bought %d %s" % (self.user, self.amount, self.crate)
