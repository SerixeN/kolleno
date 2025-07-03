import validators
from rest_framework import viewsets, status
from rest_framework.response import Response
from .constants import (
    INVALID_URL_MESSAGE,
    URL_IS_NOT_SAFE_MESSAGE,
    URL_NOT_EXIST_MESSAGE,
    URL_EXIST_MESSAGE,
    URL,
    URL_REQUIRED_MESSAGE
)
from .models import URLInformationModel
from .serializers import URLInformationSerializer
from .utils import is_safe_url, extract_url_information, normalize_url


class URLInformationViewSet(viewsets.ModelViewSet):
    queryset = URLInformationModel.objects.all()
    serializer_class = URLInformationSerializer

    def create(self, request, *args, **kwargs) -> Response:
        url = request.data.get(URL)
        if not url:
            return Response(URL_REQUIRED_MESSAGE, status.HTTP_400_BAD_REQUEST)

        normalized_url = normalize_url(url)
        if URLInformationModel.objects.filter(pk=normalized_url).exists():
            return Response(URL_EXIST_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        if not validators.url(normalized_url):
            return Response(INVALID_URL_MESSAGE, status=status.HTTP_400_BAD_REQUEST)
        if not is_safe_url(normalized_url):
            return Response(URL_IS_NOT_SAFE_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

        url_information = extract_url_information(normalized_url)
        url_information_object = URLInformationModel.objects.create(url=normalized_url, **url_information)

        return Response(self.serializer_class(url_information_object).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs) -> Response:
        try:
            url = normalize_url(kwargs[URL])
            url_information_object = self.queryset.get(pk=url)
            serializer = self.serializer_class(url_information_object)
            return Response(serializer.data)
        except self.queryset.model.DoesNotExist:
            return Response(URL_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs) -> Response:
        try:
            url = normalize_url(kwargs[URL])
            url_information_object = self.queryset.get(pk=url)
            url_information_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.queryset.model.DoesNotExist:
            return Response(URL_NOT_EXIST_MESSAGE, status=status.HTTP_404_NOT_FOUND)
