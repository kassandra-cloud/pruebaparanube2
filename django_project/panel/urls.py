from django.contrib import admin
from django.urls import path, include
from django import views
from .import views
from .views import generar_password_ajax
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('index/', views.index, name="index"),
    path('listar/', views.listar, name='listar'),
    path('agregar/', views.agregar, name='agregar'),
    path('actualizar/', views.actualizar, name='actualizar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('grupos/agregar/', views.agregar_grupo, name="agregar_grupo"),
    path('api/permisos-grupo/<int:grupo_id>/', views.obtener_permisos_por_grupo, name='obtener_permisos_por_grupo'),
    path('generar_password/', views.generar_password_ajax, name='generar_password'),
    path('', views.iniciar_admin, name='login'),  # Página principal para login
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirige a la raíz tras logout
    path('editar_grupo/<int:grupo_id>/', views.editar_grupo, name='editar_grupo'),
    path('listar_grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/eliminar/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('usuarios-inactivos/', views.listar_usuarios_inactivos, name='listar_usuarios_inactivos'),
    path('reactivar-usuario/<int:id>/', views.reactivar_usuario, name='reactivar_usuario'),
    path('monitoreo/',  views.monitoreo, name='monitoreo'),
    path('monitoreo-desempeno/', views.monitoreo_desempeno, name='monitoreo_desempeno'),
    path('api/monitoreo-desempeno/', views.api_monitoreo_desempeno, name='api_monitoreo_desempeno'),
 
]