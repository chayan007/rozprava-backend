from django.db import models

from base.models import BaseModel

from profiles.models import Profile


class Payment(BaseModel):
    """Store all payments made for the application."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.FloatField(max_length=8)
    currency = models.CharField(max_length=5)
    unique_reference_number = models.CharField(max_length=50)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    raw_order = models.JSONField(null=True)
    raw_callback = models.JSONField(null=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    extras = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.amount}'
