from email import header
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from user.models import User
from rest_framework_simplejwt.backends import TokenBackend


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user
   
    except User.DoesNotExist:
        return AnonymousUser()



class TokenAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token = headers[b'authorization']
                UntypedToken(token)

                decoded_data = TokenBackend(algorithm="HS256").decode(token, verify=False)
                scope['user'] = await get_user(validated_token=decoded_data)

            except (InvalidToken, TokenError) as e:
                 # Token is invalid
                print(e)
                scope['user'] = AnonymousUser()
           
        return await super().__call__(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
