from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaPecas, name='listaPecas'), 
    path('novo/', views.criarPeca, name='criarPeca'),
    path('editar/<int:pk>/', views.editarPeca, name='editarPeca'),
    path('deletar/<int:pk>/', views.deletarPeca, name='deletarPeca'),
]