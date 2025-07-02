import pytest
from rest_framework.test import APIClient
from urlinformation.models import URLInformationModel
from urlinformation.constants import URL_EXIST_MESSAGE, URL_IS_NOT_SAFE_MESSAGE, INVALID_URL_MESSAGE

pytestmark = pytest.mark.django_db

client = APIClient()


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

    response = client.post('/api/v1/urls/', data={'url': url}, format='json')

    assert response.status_code == 201
    assert response.data['url'] == url
    assert URLInformationModel.objects.filter(url=url).exists()


def test_create_duplicate_url():
    url = 'https://duplicate.com/'
    URLInformationModel.objects.create(url=url, domain_name='duplicate.com', protocol='https', stylesheets=0, title='')

    response = client.post('/api/v1/urls/', data={'url': url}, format='json')
    assert response.data == URL_EXIST_MESSAGE
    assert response.status_code == 400


def test_create_invalid_url():
    response = client.post('/api/v1/urls/', data={'url': 'not-a-url'}, format='json')
    assert response.data == INVALID_URL_MESSAGE
    assert response.status_code == 400


def test_create_unsafe_url(monkeypatch):
    monkeypatch.setattr('urlinformation.views.is_safe_url', lambda u: False)

    response = client.post('/api/v1/urls/', data={'url': 'https://malicious.com/'}, format='json')
    assert response.data == URL_IS_NOT_SAFE_MESSAGE
    assert response.status_code == 400
