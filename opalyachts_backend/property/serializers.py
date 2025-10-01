#this file based on REST and sends data from django to front

from rest_framework import serializers

from .models import Property


class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields=(
            'id',
            'title',
            'price_per_day',
            'image_url', 

        )