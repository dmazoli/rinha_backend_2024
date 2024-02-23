from django.db import transaction
from rest_framework.response import Response

from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from users.models import User
from users.serializers import UserSerializer, CreateTransactionSerializer, TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['transactions', 'statement']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permissions_classes = [permissions.IsAdminUser]

        return super().get_permissions()

    @transaction.atomic()
    @action(methods=['post'], detail=True, url_path='transacoes')
    def transactions(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = CreateTransactionSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='extrato')
    def statement(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = TransactionSerializer(user, data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
