from django.db import models
import uuid


class UUIDMixin(models.Model):
    id = models.UUIDField(
        editable=False, default=uuid.uuid4, primary_key=True, unique=True
    )

    class Meta:
        abstract = True


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDMixin, TimestampsMixin):
    class Meta:
        abstract = True
