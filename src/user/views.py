from functools import partial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from user.models import Citizen, Security, User, FriendRequest
from user.serializers import CitizenSerializer, RegisterCitizenSerializer, RegisterSecuritySerializer, UpdateSecuritySerializer, UserSerializer, UpdateCitizenSerializer, FriendRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission

'''
Citizen Views

'''

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        citizen = User.objects.filter(pk=request.user.id).first().citizen

        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.id == citizen.id
        else:
            return False


class RegisterCitizenView(generics.GenericAPIView):
    serializer_class = RegisterCitizenSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, citizen = serializer.save()
        
        refresh = RefreshToken.for_user(user)

        return Response(status=status.HTTP_201_CREATED, data=
            {
                
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                # 'refresh_expiry': int(refresh.lifetime.total_seconds()),
                # 'access_expiry': int(refresh.access_token.lifetime.total_seconds())   
            }
        )

class UpdateCitizenView(generics.UpdateAPIView): 
    queryset = Citizen.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UpdateCitizenSerializer

    def get_object(self):
        id = self.request.user.id

        print(self.request.body)

        return Citizen.objects.get(user=id)

# class CitizenViewSet(viewsets.ModelViewSet):
#     queryset = Citizen.objects.all()
#     serializer_class = CitizenSerializer

#     def get_permissions(self):
#         # Overrides to tightest security: Only superuser can create, update, partial update, destroy, list
#         self.permission_classes = [IsSuperUser, IsAuthenticated]

#         # Allow only by explicit exception
#         if self.action == 'retrieve':
#             self.permission_classes = [IsOwner, IsAuthenticated]

#         return super().get_permissions()


class UserProfileView(generics.GenericAPIView):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer
    permission_classes = [IsAuthenticated, IsOwner]


    # def get_permissions(self):
    #     # Overrides to tightest security: Only superuser can create, update, partial update, destroy, list
    #     self.permission_classes = [IsSuperUser, IsAuthenticated, IsOwner]
    #     # # Allow only by explicit exception
    #     # if self.action == 'retrieve':

    #     #     self.permission_classes = [IsOwner, IsAuthenticated]

    #     return super().get_permissions()

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.id).first().citizen
        serializer = self.serializer_class(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

'''
Security Views

'''


class RegisterSecurityView(generics.GenericAPIView):
    serializer_class = RegisterSecuritySerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(status=status.HTTP_201_CREATED, data=
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'refresh_expiry': int(refresh.lifetime.total_seconds()),
                'access_expiry': int(refresh.access_token.lifetime.total_seconds())
            }
        )

class UpdateSecurityView(generics.UpdateAPIView): 
    queryset = Security.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UpdateSecuritySerializer

    def get_object(self):
        id = self.request.user.id
        return Security.objects.get(user=id)


'''
Friend Request Views

'''


class CreateFriendRequestView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def post(self, request, *args,  **kwargs):
        
        sender = User.objects.filter(pk=request.user.id).first().citizen
        receiver = Citizen.objects.filter(pk=request.data.get('to_user')).first()


        if sender == receiver: 
            return Response(data={'error': 'sender cannot be the same as receiver'}, status=status.HTTP_201_CREATED)    

        friend_request_query = FriendRequest.objects.filter(from_user=sender, to_user=receiver).first()

        if friend_request_query:
            return Response(data={'error': 'friend request has already been sent'}, status=status.HTTP_400_BAD_REQUEST)


        serializer = self.serializer_class(
                data=request.data, 
                context= {
                    'sender': sender
                }
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def post(self, request, *args,  **kwargs):
        citizen = User.objects.filter(pk=request.user.id).first().citizen
        friend_request_query = FriendRequest.objects.filter(pk=request.data.get('id')).first()

        if friend_request_query.to_user == citizen:
            friend_request_query.to_user.friends.add(friend_request_query.from_user)
            friend_request_query.from_user.friends.add(citizen)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data={'error': 'friend request not accepted'}, status=status.HTTP_400_BAD_REQUEST)        