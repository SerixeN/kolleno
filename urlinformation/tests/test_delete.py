import pytest
from rest_framework.test import APIClient
from rest_framework import status
from urlinformation.models import URLInformationModel
from urlinformation.constants import URL_NOT_EXIST_MESSAGE

pytestmark = pytest.mark.django_db

client = APIClient()
TEST_URL = '/api/v1/urls/https%3A%2F%2Ftest.com%2F/'


def test_delete():
    url = 'https://test.com'
    URLInformationModel.objects.create(url=url, domain_name='test.com', protocol='https', stylesheets=0, title='')
    response = client.delete(TEST_URL)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_found():
    url = 'https://notfound.com'
    URLInformationModel.objects.create(url=url, domain_name='notfound.com', protocol='https', stylesheets=0, title='')
    response = client.delete(TEST_URL)
    assert response.data == URL_NOT_EXIST_MESSAGE
    assert response.status_code == status.HTTP_404_NOT_FOUND
