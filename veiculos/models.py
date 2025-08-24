from django.db import models
from clientes.models import Cliente

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"