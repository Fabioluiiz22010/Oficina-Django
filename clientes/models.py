#AQUI VC CRIA O MODELO DE CLIENTE NO BANCO DE DADOS

from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)  # CPF como chave primária
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"
