# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from hijack_admin.admin import HijackUserAdminMixin, HijackRelatedAdminMixin

from .models import User, Transaction, Invite


@admin.register(User)
class BartenderUserAdmin(UserAdmin, HijackUserAdminMixin):
    fieldsets = (
        (None, {"fields": ("username", "password", "telegram_id")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = UserAdmin.list_display + ("hijack_field",)


@admin.register(Transaction)
class TransactionAdmin(HijackRelatedAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "user",
        "hijack_field",
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
