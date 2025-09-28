from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaVeiculos, name='listaVeiculos'), 
    path('novo/', views.criarVeiculo, name='criarVeiculo'),
    path('editar/<str:pk>/', views.editarVeiculo, name='editarVeiculo'),
    path('deletar/<str:pk>/', views.deletarVeiculo, name='deletarVeiculo'),
]