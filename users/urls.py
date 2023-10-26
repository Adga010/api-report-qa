from django.urls import path
from . import views
from .sesion import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
]
