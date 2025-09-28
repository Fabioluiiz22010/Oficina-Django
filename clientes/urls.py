from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaClientes, name='listaClientes'),
    path('buscar_veiculo/', views.buscarVeiculo, name='buscarVeiculo'),
    path('novo/', views.criarCliente, name='criarCliente'),
    path('editar/<str:pk>/', views.editarCliente, name='editarCliente'),
    path('deletar/<str:pk>/', views.deletarCliente, name='deletarCliente'),
]