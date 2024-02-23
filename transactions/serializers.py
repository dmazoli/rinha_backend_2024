from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(label='realizado_em')

    class Meta:
        model = Transaction
        fields = '__all__'
