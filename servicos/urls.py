from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaServicos, name='listaServicos'), 
    path('novo/', views.criarServico, name='criarServico'),
    path('editar/<int:pk>/', views.editarServico, name='editarServico'),
    path('deletar/<int:pk>/', views.deletarServico, name='deletarServico'),
]