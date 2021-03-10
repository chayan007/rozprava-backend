import uuid as uuid
from django.db import models


class BaseModelManager(models.Manager):
    """Base model manager for Rozprava infrastructure."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """Base model for Rozprava infrastructure."""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created At', db_index=True
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='Last Modified At'
    )
    objects = models.Manager()
    records = BaseModelManager()

    class Meta:
        """Define meta params for model."""

        abstract = True
        ordering = ('-created_at',)
