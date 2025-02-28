# api/auth/urls_auth.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_custom import MyTokenObtainPairView
from .auth_views import register_cliente, login_cliente, get_cliente_profile_by_id

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_cliente, name='register_cliente'),
    path('login/', login_cliente, name='login_cliente'),
    path('profile/<int:id>/', get_cliente_profile_by_id, name='get_cliente_profile_by_id'),
]
