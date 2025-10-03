#this file based on REST and sends data from django to front

from rest_framework import serializers

from .models import Property
from useraccount.serializers import UserDetailSerializer

class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields=(
            'id',
            'title',
            'price_per_day',
            'image_url', 

        )

class PropertiesDetailSerializer(serializers.ModelSerializer):
    host=UserDetailSerializer(read_only=True, many=False)
    
    class Meta:
        model=Property
        fields=(
            'id',
            'title',
            'description',
            'price_per_day',
            'image_url', 
            'cabins',
            'bathrooms',
            'guests',
            'country',
            'host',

        )