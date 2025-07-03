from django.urls import path

from .views import URLInformationViewSet

urlpatterns = [
    path('v1/urls/', URLInformationViewSet.as_view({'get': 'list', 'post': 'create'}), name='url-list'),
    path('v1/urls/<path:url>/', URLInformationViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='url-detail'),
]
