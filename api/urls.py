# api/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import (
    LavagemViewSet, ExtraViewSet, VagaViewSet, AgendamentoViewSet,
    available_slots, agendar_horario
)

router = routers.DefaultRouter()
router.register(r'lavagens', LavagemViewSet)
router.register(r'extras', ExtraViewSet)
router.register(r'vagas', VagaViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('available_slots/', available_slots, name='available_slots'),
    path('agendar/', agendar_horario, name='agendar_horario'),

    # Aqui você inclui as rotas definidas em urls_auth.py
    path('auth/', include('api.auth.urls_auth')), 
]
