from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from bartender.drinks.models import Crate
from bartender.util import map_kwargs


class CrateSerializer(serializers.ModelSerializer):
    crate_price = MoneyField(max_digits=10, decimal_places=2)
    bottle_price = MoneyField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Crate
        fields = (
            "id",
            "billed",
            "billed_at",
            "billed_document",
            "created_at",
            "updated_at",
            "name",
            "crate_price",
            "bottle_price",
            "bottles",
            "calories",
            "bottle_contents",
            "bottle_calories",
        )

        extra_kwargs = map_kwargs("billed", read_only=True)
