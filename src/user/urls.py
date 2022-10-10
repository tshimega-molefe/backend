from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import CitizenViewSet, ListUsersView, RegisterCitizenView, RegisterSecurityView, UpdateCitizenView, UpdateSecurityView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'citizens', CitizenViewSet, basename='citizen')

urlpatterns = [
    path('citizen/register/', RegisterCitizenView.as_view()),
    path('security/register/', RegisterSecurityView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check/', ListUsersView.as_view()),
    #path('citizen/update/', UpdateCitizenView.as_view()),
    path('security/update/', UpdateSecurityView.as_view())
]

urlpatterns += router.urls