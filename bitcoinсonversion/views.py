from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BitcoinConversionSerializer
from .constants import BTS_API_URL, BTS_API_ERROR_MESSAGE
from .utils import get_exchange_rate
import requests


class BitcoinConversionAPIView(APIView):
    def get(self, request) -> Response:
        serializer = BitcoinConversionSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source_currency = serializer.validated_data['source_currency']
        target_currency = serializer.validated_data['target_currency']

        btc_response = requests.get(BTS_API_URL)
        if btc_response.status_code != 200:
            return Response(BTS_API_ERROR_MESSAGE, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        btc_data = btc_response.json()
        bitcoin_price = btc_data[source_currency]['last']

        try:
            exchange_rate = get_exchange_rate(source_currency, target_currency)
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

        converted_price = bitcoin_price * exchange_rate

        return Response({
            'bitcoin_price': bitcoin_price,
            'exchange_rate': exchange_rate,
            'converted_price': converted_price,
        })
