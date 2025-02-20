# core/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import LavagemViewSet, ExtraViewSet, VagaViewSet, AgendamentoViewSet

router = routers.DefaultRouter()
router.register(r'lavagens', LavagemViewSet)
router.register(r'extras', ExtraViewSet)
router.register(r'vagas', VagaViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.urls_auth')),  # <--- Importante: inclui as URLs de autenticação
]