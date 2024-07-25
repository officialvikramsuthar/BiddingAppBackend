from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email', None)
        mobile = request.data.get('mobile', None)
        if not email and not mobile:
            return Response({"error":"Email or mobile number is required."}, status=status.HTTP_204_NO_CONTENT)

        otp = "123456"  # Predefined OTP for testing
        user, created = User.objects.get_or_create(mobile=mobile, email=email, defaults={"otp": otp})

        if created:
            user.otp = otp
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})