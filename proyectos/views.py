from rest_framework import generics
from .models import Proyecto
from .serializers import ProyectoSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ProyectoList(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def perform_create(self, serializer):
        serializer.save(reportado=self.request.user)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ProyectoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def perform_update(self, serializer):
        serializer.save(reportado=self.request.user)
