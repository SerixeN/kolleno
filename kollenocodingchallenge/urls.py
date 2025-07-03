from django.urls import include, path

urlpatterns = [
    path('api/', include('urlinformation.urls')),
    path('api/', include('bitcoinсonversion.urls'))
]
