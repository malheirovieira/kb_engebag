from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base-conhecimento/', views.base_conhecimento, name='base_conhecimento'),
    path('buscar-artigos/', views.buscar_artigos, name='buscar_artigos'),
    path('artigo/<int:artigo_id>/', views.detalhe_artigo, name='detalhe_artigo'),
    path('validar-artigo/<int:artigo_id>/', views.validar_credencial_artigo, name='validar_credencial_artigo'),
    path('validar-categoria/<int:categoria_id>/', views.validar_credencial_categoria, name='validar_credencial_categoria'),
]