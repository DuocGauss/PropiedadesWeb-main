from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('propiedades/', views.listar_propiedades, name='listar'),
    path('crear_propiedad/', views.crear_propiedad, name='crear_propiedad'),
    path('editar_propiedad/<int:pk>/', views.editar_propiedad, name='editar_propiedad'),
    path('propiedades/eliminar/<int:pk>/', views.eliminar_propiedad, name='eliminar'),
    path('publicacion/', views.publicacion, name='publicacion'),
    path('crear_publicacion/<int:propiedad_id>/', views.crear_publicacion, name='crear_publicacion'),
    path('editar_publicacion/<int:id_publicacion>/', views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/eliminar_publicacion/<int:id_publicacion>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('op_venta/', views.op_venta, name='op_venta'),
    path('op_arriendo/', views.op_arriendo, name='op_arriendo'),
    path('propietarios/', views.propietarios, name='propietarios'),
    path('propietarios/editar_propietario/<int:pk>/', views.editar_propietario, name='editar_propietario'),
    path('propietarios/eliminar_propietario/<int:pk>/', views.eliminar_propietario, name='eliminar_propietario'),
    path('crear_contrato/', views.crear_contrato, name='crear_contrato'),
    path('crear_nuevo_contrato/', views.crear_nuevo_contrato, name='crear_nuevo_contrato'),
    path('agentes/', views.agentes, name='agentes'),
    path('crear_agente/', views.crear_agente, name='crear_agente'),
    path('agentes/editar_agente/<int:pk>/', views.editar_agente, name='editar_agente'),
    path('agentes/eliminar_agente/<int:pk>/', views.eliminar_agente, name='eliminar_agente'),
    path('detalles_publicacion/<int:id_publicacion>', views.detalles_publicacion, name='detalles_publicacion'),
    path('planes/', views.planes, name='planes'),
    path('imagen/<int:propiedad_id>/', views.imagen, name='imagen'),
    path('eliminar_imagen/<int:id>/', views.eliminar_imagen, name='eliminar_imagen'),
    
]


