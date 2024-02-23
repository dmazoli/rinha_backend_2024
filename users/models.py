from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from core.base_models.BaseModel import BaseModel
from core.exceptions import UnprocessableEntity


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_superuser(username, email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    limit = models.BigIntegerField(default=0)
    balance = models.IntegerField(default=0)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('id',)

    def update_balance(self, value: int, transaction_type: str) -> None:
        try:
            balance = self.balance
            new_balance = None
            if transaction_type.lower() == 'c':
                new_balance = balance + value
            elif transaction_type.lower() == 'd':
                new_balance = balance - value

            if new_balance is None:
                raise UnprocessableEntity('Valor inconsistente')

            # Limite é positivo, mas significa que o saldo, quando debitado da conta não pode execede o limite
            if abs(new_balance) > self.limit:
                raise UnprocessableEntity('Limite excedido')

            self.balance = new_balance
            self.save()

        except UnprocessableEntity as e:
            raise e

        except Exception as e:
            raise UnprocessableEntity('Erro inesperado: %s' % e)
