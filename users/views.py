from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = ()
