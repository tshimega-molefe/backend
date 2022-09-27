from rest_framework import serializers
from .models import Citizen, Security, User
from django.db import transaction

# Register serializer
class RegisterCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password = validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        role=User.Roles.CITIZEN)

        citizen = Citizen.objects.create(user=user)
        return user

class RegisterSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password = validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        role = User.Roles.SECURITY)
        
        security = Security.objects.create(user=user)
        return user

class UpdateCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('sex', 'race', 'contact_number', 'birth_date', 'image', 'home_address')

class UpdateSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = ('sex', 'race', 'contact_number', 'birth_date', 'image', 'company', 'rating')


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        
