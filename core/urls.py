from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name="home"),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/',views.registro, name='registro'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('cliente_list/', views.cliente_list, name='cliente_list'),
    path('cliente_create/', views.cliente_create, name='cliente_create'),
    path('cliente_list/cliente_update/<int:pk>/', views.cliente_update, name='cliente_update'),
    path('cliente_list/cliente_delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('clientes/add_tipo_cliente/', views.add_tipo_cliente, name='add_tipo_cliente'),
    
]
