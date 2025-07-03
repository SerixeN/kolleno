import pytest
from rest_framework.test import APIClient
from rest_framework import status
from urlinformation.models import URLInformationModel
from urlinformation.serializers import URLInformationSerializer
from urlinformation.constants import URL_NOT_EXIST_MESSAGE

pytestmark = pytest.mark.django_db

client = APIClient()
TEST_URL = '/api/v1/urls/https%3A%2F%2Ftest.com%2F/'


def test_get_one():
    url = 'https://test.com/'
    URLInformationModel.objects.create(url=url, domain_name='test.com', protocol='https', stylesheets=0, title='')
    expected = URLInformationSerializer(URLInformationModel.objects.all().get(pk=url)).data
    response = client.get(TEST_URL)
    assert response.data == expected
    assert response.status_code == status.HTTP_200_OK


def test_get_one_not_found():
    url = 'https://notfound.com/'
    URLInformationModel.objects.create(url=url, domain_name='notfound.com', protocol='https', stylesheets=0, title='')
    response = client.get(TEST_URL)
    assert response.data == URL_NOT_EXIST_MESSAGE
    assert response.status_code == status.HTTP_404_NOT_FOUND
