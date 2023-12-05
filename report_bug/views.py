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


from django.http import HttpResponse
from rest_framework.decorators import api_view
import io
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError


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
                        {
                            "detail": f"En la fila {index + 1}, el valor '{row['AREA']}' en la columna 'AREA' no es válido."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Validar CAUSAL
                if row["CAUSAL"] not in self.VALID_CAUSAL_CHOICES:
                    return Response(
                        {
                            "detail": f"En la fila {index + 1}, el valor '{row['CAUSAL']}' en la columna 'CAUSAL' no es válido."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Validar STATUS
                if row["STATUS"] not in self.VALID_STATUS_CHOICES:
                    return Response(
                        {
                            "detail": f"En la fila {index + 1}, el valor '{row['STATUS']}' en la columna 'STATUS' no es válido."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Validar SEVERIDAD
                if row["SEVERIDAD"] not in self.VALID_SEVERIDAD_CHOICES:
                    return Response(
                        {
                            "detail": f"En la fila {index + 1}, el valor '{row['SEVERIDAD']}' en la columna 'SEVERIDAD' no es válido."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                for columna in data.columns:
                    if pd.isna(row[columna]):
                        errores_celdas_vacias.append(
                            f"En la fila {index + 2}, el campo {columna} se encuentra nulo."
                        )

            # Si hay errores, devuelves un mensaje de error
            if errores_celdas_vacias:
                mensaje = " ".join(errores_celdas_vacias)
                return Response(
                    {"detalle": mensaje}, status=status.HTTP_400_BAD_REQUEST
                )

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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BugReportRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    lookup_field = "id"  # para buscar por ID

    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()  # Elimina la instancia del modelo de la base de datos
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )  # Retorna una respuesta HTTP 204 No Content


# ... API Descarga


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def download_bug_reports(request):
    # Obtener los parámetros de la URL
    fecha_inicial_str = request.query_params.get("fecha_inicial")
    fecha_final_str = request.query_params.get("fecha_final")
    project_name = request.query_params.get("project_name")
    tipo_archivo = request.query_params.get("tipo_archivo").lower()

    # Convertir las cadenas de fecha a objetos datetime y manejar errores
    try:
        fecha_inicial = datetime.strptime(fecha_inicial_str, "%Y-%m-%d")
        fecha_final = datetime.strptime(fecha_final_str, "%Y-%m-%d")
    except ValueError as e:
        # Si hay un error en el formato de fecha, retorna un mensaje de error
        return Response(
            {"detail": "Formato de fecha no válido o fecha inexistente."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Asegúrate de que la fecha_inicial no es posterior a fecha_final
    if fecha_inicial > fecha_final:
        return Response(
            {"detail": "La fecha inicial no puede ser posterior a la fecha final."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        # Verificar que el rango no exceda los 3 meses
    tres_meses = timedelta(days=90)  # Aproximadamente 3 meses
    if fecha_final - fecha_inicial > tres_meses:
        return Response(
            {"detail": "El rango de fechas no debe exceder los 3 meses."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not fecha_inicial or not fecha_final:
        return Response(
            {"detail": "Las fechas inicial y final son obligatorias."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Filtrar los datos basado en las fechas y opcionalmente en el project_name
    bug_reports_query = BugReport.objects.filter(
        FECHA__range=[fecha_inicial, fecha_final]
    )

    # Controlar el parámetro project_name
    if project_name:
        # Comprobar si hay registros para el project_name proporcionado
        if not bug_reports_query.filter(PROJECT_NAME=project_name).exists():
            # Si no hay registros, retornar que el proyecto no existe
            return Response(
                {
                    "detail": "No hay registros para el nombre del proyecto especificado."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            # Si el proyecto existe, filtra los reportes por el nombre del proyecto
            bug_reports_query = bug_reports_query.filter(PROJECT_NAME=project_name)

    # Seleccionar las columnas que quieres en tu CSV/Excel
    df = pd.DataFrame.from_records(
        bug_reports_query.values(
            "FECHA",
            "STATUS",
            "PROJECT_NAME",
            "BUG",
            "AREA",
            "CAUSAL",
            "SEVERIDAD",
            "ENLACE",
            "ENCARGADO",
            # REPORTADO es un usuario, por lo que querrás representarlo de una manera específica, p.ej., por su username
            "REPORTADO__username",
        )
    )

    # Comprobar si el DataFrame está vacío, lo que indicaría que no hay datos para ese rango de fechas

    if df.empty:
        return Response(
            {"detail": "No hay información para el rango de fechas especificado."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Convertir a Excel o CSV según el parámetro tipo_archivo
    if tipo_archivo == "excel":
        # Aquí usamos un objeto BytesIO para guardar el archivo en la memoria
        excel_io = io.BytesIO()
        with pd.ExcelWriter(excel_io, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
            # No es necesario llamar a writer.close() porque el contexto lo maneja

        # Establecer el puntero al inicio del stream
        excel_io.seek(0)
        # Crear la respuesta con el stream de BytesIO como contenido
        response = HttpResponse(
            excel_io.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        # Asegúrate de que el nombre del archivo en el Content-Disposition sea correcto
        response["Content-Disposition"] = 'attachment; filename="report.xlsx"'
        return response
    elif tipo_archivo == "csv":
        csv_io = io.StringIO()
        df.to_csv(csv_io, index=False)
        csv_io.seek(0)
        response = HttpResponse(csv_io, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=bug_reports.csv"
        return response
    else:
        return Response(
            {"detail": "Tipo de archivo no válido. Debe ser 'excel' o 'csv'."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ... API GET Dash


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_bug_reports(request):
    # Obtener los parámetros de la URL
    fecha_inicial_str = request.query_params.get("fecha_inicial")
    fecha_final_str = request.query_params.get("fecha_final")
    project_name = request.query_params.get("project_name")
    causal = request.query_params.get("causal")
    severidad = request.query_params.get("severidad").lower()
    area = request.query_params.get("area")

    # Convertir las cadenas de fecha a objetos datetime y manejar errores
    try:
        fecha_inicial = datetime.strptime(fecha_inicial_str, "%Y-%m-%d")
        fecha_final = datetime.strptime(fecha_final_str, "%Y-%m-%d")
    except ValueError:
        return Response(
            {"detail": "Formato de fecha no válido o fecha inexistente."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if fecha_inicial > fecha_final:
        return Response(
            {"detail": "La fecha inicial no puede ser posterior a la fecha final."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tres_meses = timedelta(days=90)  # Aproximadamente 3 meses
    if fecha_final - fecha_inicial > tres_meses:
        return Response(
            {"detail": "El rango de fechas no debe exceder los 3 meses."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not fecha_inicial or not fecha_final:
        return Response(
            {"detail": "Las fechas inicial y final son obligatorias."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Filtrar los datos basado en las fechas y opcionalmente en otros parámetros
    bug_reports_query = BugReport.objects.filter(
        FECHA__range=[fecha_inicial, fecha_final]
    )

    # Valores permitidos para causal, severidad y area
    causales_permitidas = [
        "Desarrollo",
        "Analisis",
        "Documentacion",
        "Testing",
        "Diseño",
    ]
    severidades_permitidas = ["Funcional", "Presentacion", "Bloqueante"]
    areas_permitidas = ["Gestion del Riesgo", "Transversal", "Mercadeo", "Axces"]

    # Controlar el parámetro causal
    if causal:
        if causal.lower() not in causales_permitidas:
            return Response(
                {"detail": "Causal no válida."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            bug_reports_query = bug_reports_query.filter(CAUSAL__iexact=causal)

    # Controlar el parámetro severidad
    if severidad:
        if severidad.lower() not in severidades_permitidas:
            return Response(
                {"detail": "Severidad no válida."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            bug_reports_query = bug_reports_query.filter(SEVERIDAD__iexact=severidad)

    # Controlar el parámetro area
    if area:
        if area.lower() not in areas_permitidas:
            return Response(
                {"detail": "Área no válida."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            bug_reports_query = bug_reports_query.filter(AREA__iexact=area)

    # # Controlar el parámetro project_name
    # if project_name:
    #     # Comprobar si hay registros para el project_name proporcionado
    #     if not bug_reports_query.filter(PROJECT_NAME=project_name).exists():
    #         # Si no hay registros, retornar que el proyecto no existe
    #         return Response(
    #             {
    #                 "detail": "No hay registros para el nombre del proyecto especificado."
    #             },
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     else:
    #         # Si el proyecto existe, filtra los reportes por el nombre del proyecto
    #         bug_reports_query = bug_reports_query.filter(PROJECT_NAME=project_name)

    # # Controlar el parámetro causal
    # if causal:
    #     # Comprobar si hay registros para el project_name proporcionado
    #     if not bug_reports_query.filter(CAUSAL=causal).exists():
    #         # Si no hay registros, retornar que el proyecto no existe
    #         return Response(
    #             {"detail": "La casual ingresada no existe."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     else:
    #         # Si el proyecto existe, filtra los reportes por el nombre del proyecto
    #         bug_reports_query = bug_reports_query.filter(CAUSAL=causal)

    # # Controlar el parámetro causal
    # if severidad:
    #     # Comprobar si hay registros para el project_name proporcionado
    #     if not bug_reports_query.filter(SEVERIDAD=severidad).exists():
    #         # Si no hay registros, retornar que el proyecto no existe
    #         return Response(
    #             {"detail": "La severidad ingresada no existe."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     else:
    #         # Si el proyecto existe, filtra los reportes por el nombre del proyecto
    #         bug_reports_query = bug_reports_query.filter(SEVERIDAD=severidad)

    # # Controlar el parámetro area
    # if area:
    #     # Comprobar si hay registros para el project_name proporcionado
    #     if not bug_reports_query.filter(AREA=area).exists():
    #         # Si no hay registros, retornar que el proyecto no existe
    #         return Response(
    #             {"detail": "La area ingresada no existe."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     else:
    #         # Si el proyecto existe, filtra los reportes por el nombre del proyecto
    #         bug_reports_query = bug_reports_query.filter(AREA=area)

    # Serializar los resultados de la consulta
    serializer = BugReportSerializer(bug_reports_query, many=True)

    # Comprobar si el conjunto de resultados está vacío
    if not bug_reports_query.exists():
        return Response(
            {"detail": "No hay información para los filtros especificados."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(serializer.data)
