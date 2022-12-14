from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections


User = get_user_model()

@database_sync_to_async
def returnUser(token_string):
    try:
        user = Token.objects.get(key=token_string).user
    except:
        user = AnonymousUser()
    return user


class AnonymousUser(AnonymousUser):
    """
    reconstruction AnonymousUser
    """
    def __init__(self):
        self.errors = []
        super().__init__()

    def add_error(self, error):
        self.errors.append(error)

    @property
    def get_errors(self):
        return self.errors


class JWTAuthMiddleware:
    def __init__(self, app):
        print('AnonymousUser')
        self.app = app

    async def __call__(self, scope, receive, send):

        close_old_connections()
        headers = dict(scope['headers'])
        try:
            if b'authorization' in headers:
                auth_header = headers[b'authorization'].decode().split()
                if len(auth_header) != 2:
                    user = AnonymousUser()
                    user.add_error('Invalid token header: no credentials provided!')
                    scope['user'] = user
                token_name, token_key = auth_header
                if token_name.lower() != 'token':
                    user = AnonymousUser()
                    user.add_error('Invalid token header: no credentials provided!')
                    scope['user'] = user
                else:
                    try:
                        user = await returnUser(token_key)
                        if user == AnonymousUser():
                            user.add_error('Token Invalid')
                        else:
                            scope['user'] = user
                    except Exception as e:
                        scope['user'] = AnonymousUser()
            else:
                user = AnonymousUser()
                user.add_error('Authentication credentials were not provided.')
                scope['user'] = user
        finally:
            return await self.app(scope, receive, send)
    
    @database_sync_to_async
    def get_user(self, token):
        try:
            user = Token.objects.get(key=token).user
        except:
            user = AnonymousUser()
        return user
    


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
