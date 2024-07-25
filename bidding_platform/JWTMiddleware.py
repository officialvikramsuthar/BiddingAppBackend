

from django.conf import settings
from UserProfile.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = JWTAuthentication()
        header = auth.get_header(request)
        if header:
            raw_token = auth.get_raw_token(header)
            if raw_token:
                try:
                    validated_token = auth.get_validated_token(raw_token)
                    user_id = validated_token.get(settings.SIMPLE_JWT['USER_ID_CLAIM'])
                    request.user = User.objects.get(id=user_id)
                except Exception as e:
                    # log the exception
                    print()

        response = self.get_response(request)
        return response

