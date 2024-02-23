from rest_framework import serializers

from core.validators.serializer_validators import StringValueValidator, StringSizeValidator
from transactions.serializers import TransactionSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    valor = serializers.IntegerField(required=True, label='value')
    tipo = serializers.CharField(required=True, validators=[StringValueValidator('c', 'd')], label='type')
    descricao = serializers.CharField(required=True, validators=[StringSizeValidator(10)], label='description')

    class Meta:
        model = User
        fields = ('valor', 'tipo', 'descricao')

    def validate(self, attrs):
        validated_attr = super().validate(attrs)
        user: User = self.instance
        user.transactions.create(value=validated_attr['valor'],
                                 transaction_type=validated_attr['tipo'],
                                 description=validated_attr['descricao'])
        return validated_attr


class UserTransactionsSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField(read_only=True, label='saldo')
    creation = serializers.DateTimeField(read_only=True, label='data_extrato')
    limit = serializers.IntegerField(read_only=True, label='limite')
    transactions = TransactionSerializer(many=True, read_only=True, label='ultimas_transacoes')

    class Meta:
        model = User
        fields = ('balance', 'creation', 'limit', 'transactions')
