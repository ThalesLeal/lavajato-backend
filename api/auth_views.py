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
    
    cliente = Cliente(email=email, nome=nome, telefone=telefone)
    cliente.set_password(password)
    cliente.save()
    
    return Response({"detail": "Cliente registrado com sucesso."},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_cliente(request):
    """
    Autentica o Cliente.
    Espera um JSON com:
    {
      "email": "cliente@example.com",
      "password": "senha123"
    }
    Retorna um token se as credenciais estiverem corretas.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({"detail": "Credenciais inválidas."},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    if cliente.check_password(password):
        token_obj, created = ClienteToken.objects.get_or_create(cliente=cliente)
        return Response({
            "token": token_obj.key,
            "email": cliente.email,
            "nome": cliente.nome,
            "telefone": cliente.telefone
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Credenciais inválidas."},
                        status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_cliente_profile(request):
    """
    Retorna os dados do Cliente logado.
    É necessário enviar o token no cabeçalho:
    Authorization: Token <seu_token>
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Token "):
        return Response({"detail": "Token não fornecido."},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    token_key = auth_header.split(" ")[1]
    try:
        token_obj = ClienteToken.objects.get(key=token_key)
    except ClienteToken.DoesNotExist:
        return Response({"detail": "Token inválido."},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    cliente = token_obj.cliente
    return Response({
        "email": cliente.email,
        "nome": cliente.nome,
        "telefone": cliente.telefone
    }, status=status.HTTP_200_OK)
