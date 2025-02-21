from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente, ClienteToken

@api_view(['POST'])
def register_cliente(request):
    """
    Registra um novo Cliente.
    Espera um JSON com:
    {
      "email": "cliente@example.com",
      "nome": "Cliente Exemplo",
      "password": "senha123",
      "telefone": "11999999999"  // opcional
    }
    """
    email = request.data.get('email')
    nome = request.data.get('nome')
    password = request.data.get('password')
    telefone = request.data.get('telefone', None)
    
    if not all([email, nome, password]):
        return Response({"detail": "Email, nome e senha são obrigatórios."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if Cliente.objects.filter(email=email).exists():
        return Response({"detail": "Email já cadastrado."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Cria o Cliente e seta a senha
    cliente = Cliente(email=email, nome=nome, telefone=telefone)
    cliente.set_password(password)
    cliente.save()
    
    return Response({"detail": "Cliente registrado com sucesso."},
                    status=status.HTTP_201_CREATED)


# api/auth_views.py
@api_view(['POST'])
def login_cliente(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({"detail": "Credenciais inválidas."}, status=401)
    
    if cliente.check_password(password):
        return Response({
            "id": cliente.id,
            "email": cliente.email,
            "nome": cliente.nome
            # etc...
        }, status=200)
    else:
        return Response({"detail": "Credenciais inválidas."}, status=401)

@api_view(['GET'])
def get_cliente_profile_by_id(request, id):
    """
    Retorna os dados do Cliente com base no id passado na URL.
    Exemplo de URL: /api/auth/profile/1/
    """
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        "id": cliente.id,
        "email": cliente.email,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "data_cadastro": cliente.data_cadastro
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cliente_profile_by_id(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente não encontrado."}, status=404)
    
    return Response({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "data_cadastro": cliente.data_cadastro
    }, status=200)
