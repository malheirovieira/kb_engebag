from django.urls import path
from .views import home, base_conhecimento

urlpatterns = [
    path('', home, name='home'),
    path('base-conhecimento/', base_conhecimento, name='base_conhecimento'),
]