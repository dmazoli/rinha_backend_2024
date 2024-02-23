from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import Transaction


@receiver(post_save, sender=Transaction)
def create_transaction(sender, instance: Transaction, created, *args, **kwargs):
    if created:
        user = instance.user
        user.update_balance(instance.value, instance.transaction_type)
