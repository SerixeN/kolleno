from enum import Enum


class SupportedCurrency(str, Enum):
    EUR = 'EUR'
    GBP = 'GBP'
    USD = 'USD'
    JPY = 'JPY'
    CHF = 'CHF'
    AUD = 'AUD'


NOT_SUPPORTED_CURRENCIES_ERROR_MESSAGE = f'Supported currencies: {', '.join([c.value for c in SupportedCurrency])}'
BTS_API_URL = 'https://blockchain.info/ticker'
BTS_API_ERROR_MESSAGE = 'Failed to fetch Bitcoin price'
ECB_API_URL_TEMPLATE = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currency}.EUR.SP00.A?startPeriod={date}'
ECB_API_ERROR_MESSAGE = 'Failed to fetch exchange rate'
