from django.urls import path
from . import views

urlpatterns = [
    path("proyectos/", views.ProyectoList.as_view(), name="proyecto-list"),
    path("proyectos/<int:pk>/", views.ProyectoDetail.as_view(), name="proyecto-detail"),
]
