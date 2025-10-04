#this file based on REST and sends data from django to front

from rest_framework import serializers

from .models import Property,Reservation
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

class ReservationsListSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)
    
    class Meta:
        model=Reservation 
        fields= (
            'id','start_date','end_date','number_of_days','total_price','property'
        )