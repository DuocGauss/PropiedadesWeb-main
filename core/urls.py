from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/',views.registro, name='registro'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]
