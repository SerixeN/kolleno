from django.urls import path
from .views import BitcoinConversionAPIView

urlpatterns = [
    path('v1/bitcoin-conversion/', BitcoinConversionAPIView.as_view(), name='bitcoin_conversion'),
]
