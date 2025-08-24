from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),  # muda para a função lista
    path('novo/', views.criar_cliente, name='criar_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('deletar/<int:pk>/', views.deletar_cliente, name='deletar_cliente'),
]
