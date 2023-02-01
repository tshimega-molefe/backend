from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserProfileView, RegisterCitizenView, RegisterSecurityView, UpdateCitizenView, UpdateSecurityView, CreateFriendRequestView, AcceptFriendRequestView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'citizen', CitizenViewSet, basename='citizen')

urlpatterns = [
    path('profile/', UserProfileView.as_view()),
    
    path('citizen/register/', RegisterCitizenView.as_view()),
    path('security/register/', RegisterSecurityView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('citizen/update/', UpdateCitizenView.as_view()),
    path('security/update/', UpdateSecurityView.as_view()),
    path('friends/send-request/', CreateFriendRequestView.as_view()),
    path('friends/accept/', AcceptFriendRequestView.as_view()),
]

urlpatterns += router.urls