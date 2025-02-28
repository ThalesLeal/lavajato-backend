# core/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import ClienteToken

class ClienteTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            return None  # Deixa para outras classes de autenticação ou retorna None
        
        try:
            token_keyword, token_key = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed("Formato do cabeçalho de token inválido.")
        
        if token_keyword.lower() != "token":
            return None

        try:
            token_obj = ClienteToken.objects.get(key=token_key)
        except ClienteToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token inválido.")
        
        # Retorna o Cliente (como usuário) e o token
        return (token_obj.cliente, token_obj)
