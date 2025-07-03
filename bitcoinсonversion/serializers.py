from rest_framework import serializers
from .constants import NOT_SUPPORTED_CURRENCIES_ERROR_MESSAGE, SupportedCurrency


class BitcoinConversionSerializer(serializers.Serializer):
    source_currency = serializers.CharField()
    target_currency = serializers.CharField()

    def validate_source_currency(self, value):
        value = value.upper()
        if value not in [c.value for c in SupportedCurrency]:
            raise serializers.ValidationError(NOT_SUPPORTED_CURRENCIES_ERROR_MESSAGE)
        return value

    def validate_target_currency(self, value):
        value = value.upper()
        if value not in [c.value for c in SupportedCurrency]:
            raise serializers.ValidationError(NOT_SUPPORTED_CURRENCIES_ERROR_MESSAGE)
        return value
