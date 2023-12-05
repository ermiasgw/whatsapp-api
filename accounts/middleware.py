from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser



@database_sync_to_async
def get_user_from_token(token_key):
    try:
        return Token.objects.get(key=token_key).user
    except Token.DoesNotExist:
        return None
 
 
class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        token = query_string.split("=")[1] if "token=" in query_string else None
        
        
        if not token:
            raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
        user = await get_user_from_token(token)
        if user:
            scope['user'] = user
        else:
            scope['user'] = AnonymousUser()
            

        return await super().__call__(scope, receive, send)