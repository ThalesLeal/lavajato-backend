# core/views.py
from rest_framework import viewsets
from .models import Lavagem, Extra, Vaga, Agendamento
from .serializers import LavagemSerializer, ExtraSerializer, VagaSerializer, AgendamentoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class LavagemViewSet(viewsets.ModelViewSet):
    queryset = Lavagem.objects.all()
    serializer_class = LavagemSerializer
    permission_classes = [IsAuthenticated]

class ExtraViewSet(viewsets.ModelViewSet):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [IsAuthenticated]

class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer
    permission_classes = [IsAdminUser]

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)
