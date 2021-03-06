import jwt
import json

from django.http import JsonResponse
from django.conf import settings

from user.models import User

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization', None)
            
            if not access_token:
                request.user = None
                return func(self, request, *args, **kwargs)

            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            login_user   = User.objects.get(id=payload['user_id'])
            request.user = login_user
            
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
    return wrapper


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({'message': 'NEED_LOGIN'}, status=401)
        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            login_user   = User.objects.get(id=payload['user_id'])
            request.user = login_user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
    return wrapper


def admin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({'message': 'NEED_LOGIN'}, status=401)

        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            login_user   = User.objects.get(id=payload['user_id'])

            if not login_user.type.name == 'admin':
                return JsonResponse({'message' : 'ACCESS_DENIED'}, status=401)
                
            request.user = login_user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

    return wrapper