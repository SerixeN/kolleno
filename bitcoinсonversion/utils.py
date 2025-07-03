from typing import AnyStr, SupportsFloat
from .constants import ECB_API_URL_TEMPLATE, ECB_API_ERROR_MESSAGE, SupportedCurrency
from datetime import date, timedelta
import requests


def get_currency_exchange_rate_from_ecb(currency: AnyStr) -> SupportsFloat:
    """
    Function to get exchange rate between currency and EUR. If source currency is EUR we return 1.0
    :param currency: currency string
    :return: exchange rate float value
    """
    if currency == SupportedCurrency.EUR.value:
        return 1.0

    yesterday = date.today() - timedelta(days=1)
    headers = {'Accept': 'application/json'}
    exchange_rate_api_response = requests.get(ECB_API_URL_TEMPLATE.format(
        currency=currency, date=yesterday.strftime('%Y-%m-%d')),
        headers=headers)

    if exchange_rate_api_response.status_code != 200:
        raise Exception(ECB_API_ERROR_MESSAGE)

    exchange_rate_json = exchange_rate_api_response.json()
    return exchange_rate_json['dataSets'][0]['series']['0:0:0:0:0']['observations']['0'][0]


def get_exchange_rate(source_currency: AnyStr, target_currency: AnyStr) -> SupportsFloat:
    """
    Function to get exchange rate between 2 currencies, since ecb target currency is EUR, we need to get 2 rates
     between currency and EUR and divide it values
    :param source_currency: source currency string
    :param target_currency: target currency string
    :return: exchange rate float value
    """
    return get_currency_exchange_rate_from_ecb(source_currency) / get_currency_exchange_rate_from_ecb(target_currency)
