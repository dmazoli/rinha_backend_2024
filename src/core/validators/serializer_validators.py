from typing import Tuple, Any

from rest_framework import serializers


class StringValueValidator:
    def __init__(self, *args):
        self.allowed_values: Tuple[Any, ...] = args

    def __call__(self, value):
        if value not in self.allowed_values:
            raise serializers.ValidationError(f'Tipo deve ser uma das opções: {", ".join(self.allowed_values)}')


class StringSizeValidator:
    def __init__(self, max_length):
        self.max_length: int = max_length

    def __call__(self, value: str):
        if len(value) > self.max_length:
            raise serializers.ValidationError(f'Descricao não deve exceder {self.max_length} caracteres')
