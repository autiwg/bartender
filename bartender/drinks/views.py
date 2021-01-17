import csv
from io import StringIO

from django.core.files.base import ContentFile
from django.db.models import Sum
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from bartender.drinks.models import Crate
from bartender.drinks.permissions import CrateAccessPolicy
from bartender.drinks.serializers import CrateSerializer
from bartender.users.models import User
from bartender.view_mixins import AccessPolicyMixin


class CrateViewSet(AccessPolicyMixin, ModelViewSet):
    serializer_class = CrateSerializer
    permission_classes = (CrateAccessPolicy,)
    queryset = Crate.objects.all()
    pagination_class = None
    filter_fields = (
        "id",
        "billed",
        "name",
        "billed_at",
        "bottles",
    )

    @action(methods=["get"], detail=True)
    def consumption(self, request, pk=None):
        crate = get_object_or_404(Crate, id=pk)
        qs = crate.transaction_set.filter(user=request.user)

        amount = qs.aggregate(sum=Sum("amount"))["sum"]

        return Response(
            {
                "amount": amount,
                "amount_total": str(amount * crate.bottle_price),
                "calories_total": ((amount * crate.bottle_contents) / 100)
                * crate.bottle_calories,
            }
        )

    @action(methods=["get"], detail=True)
    def balance(self, request, pk=None):
        crate = get_object_or_404(Crate, id=pk)
        return Response(self._get_balance_information(crate))

    def _get_balance_information(self, crate):
        qs = crate.transaction_set.all()
        amount = qs.aggregate(sum=Sum("amount"))["sum"]
        staff_users_count = User.objects.filter(is_staff=True).count()
        return {
            "crate_price": str(crate.crate_price),
            "crate_bottle_price": str(crate.bottle_price),
            "crate_bottle_price_markup": str(crate.bottle_price_markup),
            "crate_bottles": crate.bottles,
            "crate_bottles_purchased": amount,
            "crate_bottles_purchased_amount": str(amount * crate.bottle_price),
            "crate_bottle_difference": amount - crate.bottles,
            "crate_bottle_ratio": amount / crate.bottles,
            "crate_open_amount": str(crate.crate_price - (amount * crate.bottle_price)),
            "staff_amount": staff_users_count,
            "staff_open_amount_split": str(
                (crate.crate_price - (amount * crate.bottle_price)) / staff_users_count
            ),
        }

    @action(methods=["post"], detail=True)
    def bill(self, request, pk=None):
        crate = get_object_or_404(Crate, id=pk)
        crate.billed = True
        data = self._get_balance_information(crate)
        csv_buffer = StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=data.keys())
        csv_writer.writeheader()
        csv_writer.writerow(data)
        csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8"))
        crate.billed_document.save(name="export.csv", content=csv_file)
        crate.save()
        return redirect(reverse("crate-detail", [crate.id]))
