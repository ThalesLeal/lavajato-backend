from django.urls import path
from .auth_views import register_cliente, login_cliente, get_cliente_profile_by_id

urlpatterns = [
    path('register/', register_cliente, name='register'),  # /api/auth/register/
    path('login/', login_cliente, name='login'),          # /api/auth/login/
    #path('profile/', get_cliente_profile, name='profile') # /api/auth/profile/
    path('profile/<int:id>/', get_cliente_profile_by_id, name='profile_by_id'),
]
