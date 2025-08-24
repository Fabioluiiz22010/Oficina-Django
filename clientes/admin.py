#AQUI VC REGISTRA O MODELO DE CLIENTE NO ADMIN DO DJANGO PARA GERENCIAR OS CLIENTES PELA INTERFACE DO ADMIN
from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)
