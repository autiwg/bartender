from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField

from bartender import settings
from bartender.mixins import BaseModel


class Crate(BaseModel):
    billed = models.BooleanField(
        default=False,
        verbose_name="Crate billed",
        help_text="Whether this crate has been billed/emptied",
    )
    billed_at = models.DateTimeField(null=True, blank=True, editable=False)

    name = models.CharField(max_length=255, verbose_name="Crate name")
    crate_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=getattr(settings, "DEFAULT_CURRENCY", "EUR"),
        verbose_name="Price per crate",
    )
    bottles = models.IntegerField(
        verbose_name="Amount of bottles per crate",
        validators=[
            MinValueValidator(1, "There has to be at least one bottle per crate")
        ],
    )

    calories = models.IntegerField(verbose_name="Kcal per 100ml", null=True, blank=True)
    bottle_contents = models.IntegerField(
        verbose_name="Bottle contents in ml", default=500
    )
    bottle_price_markup = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency=getattr(settings, "DEFAULT_CURRENCY", "EUR"),
        verbose_name="Price markup per bottle",
        default=0,
    )

    @property
    def bottle_price(self):
        """Returns the price per bottle"""
        return (self.crate_price / self.bottles) + self.bottle_price_markup

    @property
    def bottle_calories(self):
        if self.calories:
            return self.calories * (self.bottle_contents / 100)
        return 0

    def __str__(self):
        if self.billed:
            return "(billed at %s) %s" % (self.billed_at, self.name)
        return self.name
