from rest_framework import serializers

from core.validators.serializer_validators import StringValueValidator, StringSizeValidator
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    valor = serializers.IntegerField(required=True)
    tipo = serializers.CharField(required=True, validators=[StringValueValidator('c', 'd')])
    descricao = serializers.CharField(required=True, validators=[StringSizeValidator(10)])

    class Meta:
        model = User
        fields = ('valor', 'tipo', 'descricao')

    def validate(self, attrs):
        validated_attr = super().validate(attrs)
        user: User = self.instance
        Transaction.objects.create(user=user,
                                   value=validated_attr['valor'],
                                   transaction_type=validated_attr['tipo'],
                                   description=validated_attr['descricao'])
        self.instance.refresh_from_db()
        return self.to_api_view()

    def to_api_view(self) -> dict:
        dict_value = dict()
        dict_value['saldo'] = self.instance.balance
        dict_value['limite'] = self.instance.limit

        return dict_value


class UserTransactionsSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField(read_only=True, label='saldo')
    creation = serializers.DateTimeField(read_only=True, label='data_extrato')
    limit = serializers.IntegerField(read_only=True, label='limite')
    transactions = TransactionSerializer(many=True, read_only=True, label='ultimas_transacoes')

    class Meta:
        model = User
        fields = ('balance', 'creation', 'limit', 'transactions')
