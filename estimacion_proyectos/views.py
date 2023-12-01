from rest_framework import generics
from .models import EstimacionProyecto
from .serializers import EstimacionProyectoSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class EstimacionProyectoListCreate(generics.ListCreateAPIView):
    queryset = EstimacionProyecto.objects.all()
    serializer_class = EstimacionProyectoSerializer
