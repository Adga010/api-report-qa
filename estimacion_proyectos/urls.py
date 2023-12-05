from django.urls import path
from .views import EstimacionProyectoListCreate

urlpatterns = [
    path(
        "estimaciones/",
        EstimacionProyectoListCreate.as_view(),
        name="estimacion-proyecto-list-create",
    ),
]
