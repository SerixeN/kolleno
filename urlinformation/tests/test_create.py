import pytest
from rest_framework.test import APIClient
from rest_framework import status
from urlinformation.models import URLInformationModel
from urlinformation.utils import normalize_url
from urlinformation.constants import (
    URL_EXIST_MESSAGE,
    URL_IS_NOT_SAFE_MESSAGE,
    INVALID_URL_MESSAGE,
    URL_REQUIRED_MESSAGE
)


pytestmark = pytest.mark.django_db

client = APIClient()
TEST_URL = '/api/v1/urls/'


def test_create_success(monkeypatch):
    url = 'https://example.com/'

    monkeypatch.setattr('urlinformation.views.is_safe_url', lambda u: True)
    monkeypatch.setattr('urlinformation.views.extract_url_information', lambda u: {
        'domain_name': 'example.com',
        'protocol': 'https',
        'title': 'Test Title',
        'images': ['https://example.com/image.png'],
        'stylesheets': 2,
    })

    response = client.post(TEST_URL, data={'url': url}, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['url'] == normalize_url(url)
    assert URLInformationModel.objects.filter(url=normalize_url(url)).exists()


def test_create_missed_url(monkeypatch):
    monkeypatch.setattr('urlinformation.views.is_safe_url', lambda u: False)

    response = client.post(TEST_URL)
    assert response.data == URL_REQUIRED_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_duplicate_url():
    url = 'https://duplicate.com'
    URLInformationModel.objects.create(url=url, domain_name='duplicate.com', protocol='https', stylesheets=0, title='')

    response = client.post(TEST_URL, data={'url': url}, format='json')
    assert response.data == URL_EXIST_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_url():
    response = client.post(TEST_URL, data={'url': 'not-a-url'}, format='json')
    assert response.data == INVALID_URL_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_unsafe_url(monkeypatch):
    monkeypatch.setattr('urlinformation.views.is_safe_url', lambda u: False)

    response = client.post(TEST_URL, data={'url': 'https://malicious.com/'}, format='json')
    assert response.data == URL_IS_NOT_SAFE_MESSAGE
    assert response.status_code == status.HTTP_400_BAD_REQUEST
