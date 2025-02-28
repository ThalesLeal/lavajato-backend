# core/models.py
from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class ClienteManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class Cliente(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=80)
    senha = models.CharField(max_length=128)  # Senha armazenada com hash
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Atributos esperados pelo sistema de autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = ClienteManager()

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)
    
    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

class ClienteToken(models.Model):
    """
    Modelo simples para armazenar um token associado a um Cliente.
    """
    key = models.CharField(max_length=40, primary_key=True, editable=False)
    cliente = models.OneToOneField(Cliente, related_name='cliente_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
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
    # O campo cliente faz referência ao nosso modelo personalizado Cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
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
        return f"{self.cliente.nome} - {self.data_agendamento} {self.horario}"
