import pytest
from rest_framework.test import APIClient
from rest_framework import status
from bitcoinсonversion.constants import SupportedCurrency


TEST_URL = '/api/v1/bitcoin-conversion/'


@pytest.fixture
def client():
    return APIClient()


def test_successful_conversion(client, monkeypatch):
    def mock_btc_api(url):
        class MockResponse:
            status_code = 200

            def json(self):
                return {
                    SupportedCurrency.USD.value: {'last': 50000},
                    SupportedCurrency.GBP.value: {'last': 45000},
                }
        return MockResponse()

    def mock_get_exchange_rate(src, tgt):
        return 0.8

    monkeypatch.setattr('bitcoinсonversion.views.requests.get', mock_btc_api)
    monkeypatch.setattr('bitcoinсonversion.views.get_exchange_rate', mock_get_exchange_rate)

    response = client.get(TEST_URL, {'source_currency': SupportedCurrency.USD.value,
                                     'target_currency': SupportedCurrency.GBP.value})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['bitcoin_price'] == 50000
    assert response.data['exchange_rate'] == 0.8
    assert response.data['converted_price'] == 50000 * 0.8


def test_invalid_params(client):
    response = client.get(TEST_URL, {'source_currency': 'INVALID'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_btc_api_failure(client, monkeypatch):
    def mock_btc_api(url):
        class MockResponse:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            def json(self):
                return {}
        return MockResponse()

    monkeypatch.setattr('bitcoinсonversion.views.requests.get', mock_btc_api)

    response = client.get(TEST_URL, {'source_currency': SupportedCurrency.USD.value,
                                     'target_currency': SupportedCurrency.GBP.value})
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


def test_ecb_api_failure(client, monkeypatch):
    def mock_btc_api(url):
        class MockResponse:
            status_code = status.HTTP_200_OK

            def json(self):
                return {
                    'USD': {'last': 50000},
                    'GBP': {'last': 45000},
                }
        return MockResponse()

    def mock_get_exchange_rate(src, tgt):
        raise Exception('ECB API failed')

    monkeypatch.setattr('bitcoinсonversion.views.requests.get', mock_btc_api)
    monkeypatch.setattr('bitcoinсonversion.views.get_exchange_rate', mock_get_exchange_rate)

    response = client.get(TEST_URL, {'source_currency': SupportedCurrency.USD.value,
                                     'target_currency': SupportedCurrency.GBP.value})
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert 'ECB API failed' in response.data
