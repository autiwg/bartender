# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Crate


@admin.register(Crate)
class CrateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "billed",
        "billed_at",
        "billed_document",
        "crate_price",
        "bottles",
        "calories",
        "bottle_contents",
    )
    list_filter = (
        "billed",
        "created_at",
        "updated_at",
        "bottles",
    )
    search_fields = ("name",)
    date_hierarchy = "created_at"
