from rest_framework import serializers
from .models import URLInformationModel


class URLInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLInformationModel
        fields = '__all__'
