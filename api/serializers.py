# core/serializers.py
from rest_framework import serializers
from .models import Lavagem, Extra, Vaga, Agendamento
# api/auth/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LavagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lavagem
        fields = '__all__'

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):
    lavagem = LavagemSerializer(read_only=True)
    extras = ExtraSerializer(read_only=True, many=True)
    lavagem_id = serializers.PrimaryKeyRelatedField(queryset=Lavagem.objects.all(), write_only=True)
    extras_ids = serializers.PrimaryKeyRelatedField(queryset=Extra.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Agendamento
        fields = ('id', 'cliente', 'lavagem', 'lavagem_id', 'extras', 'extras_ids', 'data_agendamento', 'horario', 'status')

    def validate(self, data):
        data_agendamento = data.get('data_agendamento')
        horario = data.get('horario')
        lavagem = data.get('lavagem_id')
        
        # Validação: busca vaga para o horário
        from .models import Vaga, Agendamento
        vaga = Vaga.objects.filter(
            data=data_agendamento, 
            hora_inicio__lte=horario, 
            hora_fim__gte=horario
        ).first()
        if not vaga:
            raise serializers.ValidationError("Não há vaga disponível neste horário.")

        agendamentos_no_horario = Agendamento.objects.filter(
            data_agendamento=data_agendamento, 
            horario=horario
        ).count()
        if agendamentos_no_horario >= vaga.quantidade:
            raise serializers.ValidationError("Vaga esgotada para este horário.")

        # Verifica se o tempo estimado cabe dentro do período da vaga
        from datetime import datetime
        tempo_estimado = lavagem.tempo_estimado
        horario_datetime = datetime.combine(data_agendamento, horario)
        hora_fim_vaga = datetime.combine(data_agendamento, vaga.hora_fim)
        if horario_datetime + tempo_estimado > hora_fim_vaga:
            raise serializers.ValidationError("O tempo estimado da lavagem extrapola o horário da vaga.")

        return data

    def create(self, validated_data):
        lavagem = validated_data.pop('lavagem_id')
        extras = validated_data.pop('extras_ids', [])
        agendamento = Agendamento.objects.create(lavagem=lavagem, **validated_data)
        if extras:
            agendamento.extras.set(extras)
        return agendamento
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Substitui o campo "username" pelo "email"
        # Assim, o usuário pode enviar "email" no corpo da requisição.
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
