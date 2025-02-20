# core/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.hashers import make_password, check_password

class Cliente(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=80)
    senha = models.CharField(max_length=128)  # senha armazenada com hash
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)
    
    def __str__(self):
        return self.email

class ClienteToken(models.Model):
    """
    Modelo simples para armazenar um token associado a um Cliente.
    """
    key = models.CharField(max_length=40, primary_key=True, editable=False)
    cliente = models.OneToOneField(Cliente, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            # Gera um token aleatório usando uuid4 (hexadecimal)
            self.key = uuid.uuid4().hex
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key


class Lavagem(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    tempo_estimado = models.DurationField()  # Ex.: 00:30:00

    def __str__(self):
        return self.nome

class Extra(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome

class Vaga(models.Model):
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.data} - {self.hora_inicio} até {self.hora_fim}"

class Agendamento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    lavagem = models.ForeignKey(Lavagem, on_delete=models.CASCADE)
    extras = models.ManyToManyField(Extra, blank=True)
    data_agendamento = models.DateField()
    horario = models.TimeField()
    status = models.CharField(
        max_length=20, 
        choices=(
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('cancelado', 'Cancelado'),
        ),
        default='pendente'
    )

    def __str__(self):
        return f"{self.cliente.username} - {self.data_agendamento} {self.horario}"
