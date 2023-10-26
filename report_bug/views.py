from rest_framework import generics, status
from rest_framework.response import Response
from .models import BugReport
from .serializers import BugReportSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .serializers import FileUploadSerializer


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BugReportListCreateView(generics.ListCreateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    lookup_field = "id"  # para buscar por ID

    def create(self, request, *args, **kwargs):
        # Tomar el usuario autenticado a partir del token
        user = self.request.user
        # Añadir el usuario al request.data
        data = request.data.copy()
        data["REPORTADO"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request):
        bugs = BugReport.objects.all()
        serializer = BugReportSerializer(bugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BugReportRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    lookup_field = "id"  # para buscar por ID

    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )  # 'partial=True' permite actualizaciones parciales
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BugReportFileUploadView(APIView):
    parser_classes = [MultiPartParser]
    
    VALID_AREA_CHOICES = [choice[0] for choice in BugReport.AREA_CHOICES]
    VALID_CAUSAL_CHOICES = [choice[0] for choice in BugReport.CAUSAL_CHOICES]
    VALID_STATUS_CHOICES = [choice[0] for choice in BugReport.STATUS_CHOICES]
    VALID_SEVERIDAD_CHOICES = [choice[0] for choice in BugReport.SEVERIDAD_CHOICES]


    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data["file"]
            data = pd.read_excel(file, engine="openpyxl")

            # Lista para guardar los errores de celdas vacías
            errores_celdas_vacias = []

            # Iterar sobre todas las filas y columnas y verificar celdas vacías
            for index, row in data.iterrows():
                
                
                # Validar AREA
                if row["AREA"] not in self.VALID_AREA_CHOICES:
                    return Response(
                        {"detail": f"En la fila {index + 1}, el valor '{row['AREA']}' en la columna 'AREA' no es válido."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validar CAUSAL
                if row["CAUSAL"] not in self.VALID_CAUSAL_CHOICES:
                    return Response(
                        {"detail": f"En la fila {index + 1}, el valor '{row['CAUSAL']}' en la columna 'CAUSAL' no es válido."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validar STATUS
                if row["STATUS"] not in self.VALID_STATUS_CHOICES:
                    return Response(
                        {"detail": f"En la fila {index + 1}, el valor '{row['STATUS']}' en la columna 'STATUS' no es válido."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validar SEVERIDAD
                if row["SEVERIDAD"] not in self.VALID_SEVERIDAD_CHOICES:
                    return Response(
                        {"detail": f"En la fila {index + 1}, el valor '{row['SEVERIDAD']}' en la columna 'SEVERIDAD' no es válido."},
                        status=status.HTTP_400_BAD_REQUEST
        )
                for columna in data.columns:
                    if pd.isna(row[columna]):
                        errores_celdas_vacias.append(f"En la fila {index + 2}, el campo {columna} se encuentra nulo.")

            # Si hay errores, devuelves un mensaje de error
            if errores_celdas_vacias:
                mensaje = " ".join(errores_celdas_vacias)
                return Response({"detalle": mensaje}, status=status.HTTP_400_BAD_REQUEST)

            # Si todo está bien, procesas el archivo
            for index, row in data.iterrows():
                BugReport.objects.create(
                    FECHA=row["FECHA"],
                    STATUS=row["STATUS"],
                    PROJECT_NAME=row["PROJECT_NAME"],
                    BUG=row["BUG"],
                    AREA=row["AREA"],
                    CAUSAL=row["CAUSAL"],
                    SEVERIDAD=row["SEVERIDAD"],
                    ENLACE=row["ENLACE"],
                    ENCARGADO=row["ENCARGADO"],
                    REPORTADO=request.user,
                )

            return Response(
                {"status": "success", "message": "Data uploaded successfully"},
                status=201,
            )
        else:
            return Response(serializer.errors, status=400)

