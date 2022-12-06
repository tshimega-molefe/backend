from functools import partial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from user.models import Citizen, Security, User, FriendRequest
from user.serializers import CitizenSerializer, RegisterCitizenSerializer, RegisterSecuritySerializer, UpdateSecuritySerializer, UserSerializer, UpdateCitizenSerializer, FriendRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import action


'''
Citizen Views

'''

class RegisterCitizenView(generics.GenericAPIView):
    serializer_class = RegisterCitizenSerializer

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

class UpdateCitizenView(generics.UpdateAPIView): 
    queryset = Citizen.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UpdateCitizenSerializer

    def get_object(self):
        id = self.request.user.id
        return Citizen.objects.get(user=id)

class CitizenViewSet(viewsets.ModelViewSet):
    queryset = Citizen.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = CitizenSerializer

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

        print(citizen.friends.all())
        if friend_request_query.to_user == citizen:

            friend_request_query.to_user.friends.add(friend_request_query.from_user)
            friend_request_query.from_user.friends.add(citizen)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data={'error': 'friend request not accepted'}, status=status.HTTP_400_BAD_REQUEST)

        
        