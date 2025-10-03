from rest_framework import serializers 

from .models import User

class UserDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(default='Oussema')
    class Meta:
        model= User
        fields=(
            'id','name','avatar'
        )