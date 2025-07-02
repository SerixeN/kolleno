import pytest
from rest_framework.test import APIClient
from urlinformation.models import URLInformationModel
from urlinformation.serializers import URLInformationSerializer

pytestmark = pytest.mark.django_db

client = APIClient()


def test_get_list():
    url = 'https://test.com/'
    URLInformationModel.objects.create(url=url, domain_name='test.com', protocol='https', stylesheets=0, title='')
    expected = [URLInformationSerializer(item).data for item in URLInformationModel.objects.all()]
    response = client.get('/api/v1/urls/')
    assert response.data == expected
    assert response.status_code == 200
