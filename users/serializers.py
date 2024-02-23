import datetime

from django.utils import timezone
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
    balance = serializers.IntegerField(read_only=True, required=False)
    creation = serializers.DateTimeField(read_only=True, required=False)
    limit = serializers.IntegerField(read_only=True, required=False)
    transactions = TransactionSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('balance', 'creation', 'limit', 'transactions')

    def validate(self, attrs):
        super().validate(attrs)
        return self.to_api_view()

    def to_api_view(self) -> dict:
        dict_value = dict()
        dict_value['saldo'] = {
            'total': self.instance.balance,
            'data_extrato': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'limite': self.instance.limit
        }
        last_transactions_list = self.instance.transactions.order_by('created_at')[:10].values_list('id', flat=True)

        last_transactions = TransactionSerializer(
            self.instance.transactions.filter(id__in=last_transactions_list).order_by('created_at'),
            many=True
        ).data
        dict_value['ultimas_transacoes'] = list(map(self.convert_transactions_data, last_transactions))
        return dict_value

    @staticmethod
    def convert_transactions_data(data: dict) -> dict:
        return {
            'valor': data.get('value'),
            'tipo': data.get('transaction_type'),
            'descricao': data.get('description'),
            'realizada_em': data.get('created_at')
        }
