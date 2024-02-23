from django.db import models

from core.base_models.BaseModel import BaseModel
from users.models import User


class TransactionTypes:
    CREDIT = 'c'
    DEBIT = 'd'

    CHOICES = [
        (CREDIT, CREDIT),
        (DEBIT, DEBIT)
    ]


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    value = models.IntegerField(blank=False, null=False)
    transaction_type = models.CharField(max_length=1, blank=False, null=False, choices=TransactionTypes.CHOICES)
    description = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        ordering = ('created_at',)
