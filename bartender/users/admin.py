# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Transaction, Invite

admin.site.register(User, UserAdmin)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "updated_at",
        "user",
        "crate",
        "amount",
    )
    list_filter = ("created_at", "updated_at", "user", "crate")
    date_hierarchy = "created_at"


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at", "created_by", "token")
    list_filter = ("created_at", "updated_at", "created_by")
    date_hierarchy = "created_at"
