from django.db import models
from veiculos.models import Veiculo
from servicos.models import Servico
from pecas.models import Peca

class OrdemServico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='ordens_servico') # Relacionamento com Veiculo
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='ordens_servico') #' Relacionamento com Servico
    pecas = models.ManyToManyField(Peca, blank=True, related_name='ordens_servico') # Relacionamento com Peca
    Kilometragem = models.PositiveIntegerField() # Quilometragem do veículo
    dataEntrada = models.DateField(auto_now_add=True) # Data de entrada automática
    dataSaida = models.DateField(blank=True, null=True) # Data de saída opcional
    feito = models.BooleanField(default=False) # Indica se o serviço foi concluído
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Valor total do serviço

    def __str__(self):
        return f"{self.veiculo} ({self.servico})"
