from django.urls import path
from . import views
from .views import galeria, comentar


urlpatterns = [
    path('', views.galeria, name='galeria'),  # Aquí se accede a fotos/ y carga la vista 'galeria'
    path('comentar/<int:foto_id>/', views.comentar, name='comentar'),
    path('subir/', views.subir_foto, name='subir_foto'),  # Nueva URL para subir fotos
    path('acceso/', views.acceso, name='acceso'),  # Ruta para la vista 'acceso'
    path('borrar_foto/<int:foto_id>/', views.borrar_foto, name='borrar_foto'),  # URL para borrar foto
]
