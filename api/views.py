# core/views.py
from rest_framework import viewsets
from .models import Lavagem, Extra, Vaga, Agendamento
from .serializers import LavagemSerializer, ExtraSerializer, VagaSerializer, AgendamentoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime

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
        # Assume que request.user está configurado (integração com sistema de autenticação)
        serializer.save(cliente=self.request.user)

@api_view(['GET'])
def available_slots(request):
    """
    Retorna os horários disponíveis para uma data específica.
    Exemplo de chamada: GET /api/available_slots?date=2025-02-26
    Para cada hora das 08:00 às 18:00, verifica se já existe um agendamento.
    Retorna um array de objetos: { id, hora, ocupado }
    """
    date_str = request.query_params.get('date')
    if not date_str:
        return Response({"detail": "Parâmetro 'date' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"detail": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    slots = []
    for hour in range(8, 19):  # das 08:00 até as 18:00
        time_obj = datetime.time(hour, 0)
        ocupado = Agendamento.objects.filter(data_agendamento=date_obj, horario=time_obj).exists()
        slots.append({
            "id": int(f"{date_obj.day}{hour}"),
            "hora": f"{hour:02d}:00",
            "ocupado": ocupado
        })
    
    return Response(slots, status=status.HTTP_200_OK)

@api_view(['POST'])
def agendar_horario(request):
    """
    Cria um agendamento.
    Espera JSON:
    {
      "date": "YYYY-MM-DD",
      "hora": "HH:MM",
      "tipoLavagem": "Simples",
      "placa": "ABC-1234"
    }
    """
    date_str = request.data.get("date")
    hora_str = request.data.get("hora")
    tipoLavagem = request.data.get("tipoLavagem")
    placa = request.data.get("placa")
    
    if not all([date_str, hora_str, tipoLavagem, placa]):
        return Response({"detail": "Todos os parâmetros são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        hour, minute = map(int, hora_str.split(":"))
        time_obj = datetime.time(hour, minute)
    except Exception:
        return Response({"detail": "Formato de data ou hora inválido."}, status=status.HTTP_400_BAD_REQUEST)
    
    if Agendamento.objects.filter(data_agendamento=date_obj, horario=time_obj).exists():
        return Response({"detail": "Horário já ocupado."}, status=status.HTTP_400_BAD_REQUEST)
    
    lavagem = Lavagem.objects.first()
    if not lavagem:
        return Response({"detail": "Nenhuma lavagem disponível no sistema."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Cria o agendamento – note que usamos request.user; certifique-se de que o usuário está autenticado.
    Agendamento.objects.create(
        cliente=request.user,
        lavagem=lavagem,
        data_agendamento=date_obj,
        horario=time_obj,
        status="pendente"
    )
    return Response({"detail": "Agendamento criado com sucesso."}, status=status.HTTP_201_CREATED)
