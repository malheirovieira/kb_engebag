from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base-conhecimento/', views.base_conhecimento, name='base_conhecimento'),
    # Esta linha é importante para o clique funcionar:
    path('artigo/<int:artigo_id>/', views.detalhe_artigo, name='detalhe_artigo'),
    path('busca/', views.buscar_artigos, name='buscar_artigos'),
]