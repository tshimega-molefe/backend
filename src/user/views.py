from functools import partial
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from user.models import Citizen, Security, User
from user.serializers import RegisterCitizenSerializer, RegisterSecuritySerializer, UpdateSecuritySerializer, UserSerializer, UpdateCitizenSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterCitizenView(generics.GenericAPIView):
    serializer_class = RegisterCitizenSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(status=status.HTTP_201_CREATED, data=
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )

class RegisterSecurityView(generics.GenericAPIView):
    serializer_class = RegisterSecuritySerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(status=status.HTTP_201_CREATED, data=
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )


class UpdateCitizenView(generics.UpdateAPIView): 
    queryset = Citizen.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UpdateCitizenSerializer

    def get_object(self):
        id = self.request.user.id
        return Citizen.objects.get(user=id)

class UpdateSecurityView(generics.UpdateAPIView): 
    queryset = Security.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UpdateSecuritySerializer

    def get_object(self):
        id = self.request.user.id
        return Security.objects.get(user=id)


class ListUsersView(generics.ListAPIView): 
    queryset = User.objects.all()
 
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()