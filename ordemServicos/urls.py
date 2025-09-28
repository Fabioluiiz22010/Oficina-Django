from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaOrdens, name='listaOrdens'),
    path('novo/', views.criarOrdem, name='criarOrdem'),
    path('editar/<int:pk>/', views.editarOrdem, name='editarOrdem'),
    path('deletar/<int:pk>/', views.deletarOrdem, name='deletarOrdem'),
]