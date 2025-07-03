import pytest
from bitcoinсonversion.utils import get_currency_exchange_rate_from_ecb, get_exchange_rate
from bitcoinсonversion.constants import SupportedCurrency, ECB_API_ERROR_MESSAGE


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


@pytest.fixture
def mock_ecb_response(monkeypatch):
    def mock_get(url, headers):
        if SupportedCurrency.USD.value in url:
            return MockResponse(200, {
                'dataSets': [{
                    'series': {
                        '0:0:0:0:0': {
                            'observations': {
                                '0': [1.2]
                            }
                        }
                    }
                }]
            })
        if SupportedCurrency.GBP.value in url:
            return MockResponse(200, {
                'dataSets': [{
                    'series': {
                        '0:0:0:0:0': {
                            'observations': {
                                '0': [0.85]
                            }
                        }
                    }
                }]
            })
    monkeypatch.setattr('bitcoinсonversion.utils.requests.get', mock_get)


def test_get_currency_exchange_rate_from_ecb(mock_ecb_response):
    rate = get_currency_exchange_rate_from_ecb(SupportedCurrency.USD.value)
    assert rate == 1.2


def test_get_exchange_rate(mock_ecb_response):
    rate = get_exchange_rate(SupportedCurrency.USD.value, SupportedCurrency.GBP.value)
    assert round(rate, 4) == round(1.2 / 0.85, 4)


def test_get_currency_exchange_rate_from_ecb_eur_direct():
    rate = get_currency_exchange_rate_from_ecb(SupportedCurrency.EUR.value)
    assert rate == 1.0


def test_raises_on_non_200_response(monkeypatch):
    class MockResponse:
        status_code = 500

        def json(self):
            return {}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr('bitcoinсonversion.utils.requests.get', mock_get)

    with pytest.raises(Exception) as exc_info:
        get_currency_exchange_rate_from_ecb(SupportedCurrency.USD.value)

    assert ECB_API_ERROR_MESSAGE in str(exc_info.value)
