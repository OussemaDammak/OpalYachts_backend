from rest_framework import serializers 

from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer



class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

    def save(self, request):
        # Call super() to handle password hashing and user creation
        user = super().save(request)
        # Update the 'name' field (if not already set)
        user.name = self.validated_data.get('name', '')
        user.save()
        return user
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=(
            'id','name'
        )
        