# core/auth_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status# Dentro de api/auth/auth_views.py
from api.models import Cliente, ClienteToken


@api_view(['POST'])
def register_cliente(request):
    """
    Registra um novo Cliente.
    Espera JSON:
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
    
    cliente = Cliente(email=email, nome=nome, telefone=telefone)
    cliente.set_password(password)
    cliente.save()
    
    return Response({"detail": "Cliente registrado com sucesso."},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_cliente(request):
    """
    Autentica um cliente.
    Espera JSON:
    {
      "email": "cliente@example.com",
      "password": "senha123"
    }
    Retorna os dados do cliente e o token.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
    
    if cliente.check_password(password):
        token_obj, created = ClienteToken.objects.get_or_create(cliente=cliente)
        return Response({
            "id": cliente.id,
            "email": cliente.email,
            "nome": cliente.nome,
            "token": token_obj.key
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_cliente_profile_by_id(request, id):
    """
    Retorna os dados do cliente com base no ID.
    Exemplo: GET /api/auth/profile/1/
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