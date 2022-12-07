from rest_framework import serializers
from .models import Citizen, Security, User, FriendRequest
from django.db import transaction

# Register serializer
class RegisterCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        required_fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password = validated_data['password'],
                                        role=User.Roles.CITIZEN)

        citizen = Citizen.objects.create(user=user)
        return user, citizen

class UpdateCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('sex', 'race', 'contact_number', 'birth_date', 'image', 'home_address')

class RegisterSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password','first_name', 'last_name')
        required_fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password = validated_data['password'],
                                        role = User.Roles.SECURITY)
        
        security = Security.objects.create(user=user)
        return user


class UpdateSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = ('sex', 'race', 'contact_number', 'birth_date', 'image', 'company', 'rating')

# User serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CitizenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = serializers.SerializerMethodField()

    def get_friends(self, instance):

        friends = instance.friends.all()
        friend_list = []
        for friend in friends:
            friend_list.append({'username': friend.user.username, 'first_name': friend.user.first_name, 'lasts_name': friend.user.last_name})
        
        return friend_list


    class Meta: 
        model = Citizen
        fields = '__all__'


class SecuritySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta: 
        model = Security
        fields = '__all__'

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FriendRequest
        fields = '__all__'
        optional_fields = ['to_user']
        read_only_fields = ['from_user', 'id']

    def create(self, validated_data):
        '''Friend Request Send'''
        friend_request = FriendRequest(from_user=self.context.get('sender'), **validated_data)
        friend_request.save()

        return friend_request


