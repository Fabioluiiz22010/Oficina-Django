from django.db import models
from veiculos.models import Veiculo
from servicos.models import Servico
from pecas.models import Peca

class PecaUsada(models.Model):
    ordemServico = models.ForeignKey('OrdemServico', on_delete=models.CASCADE)
    peca = models.ForeignKey(Peca, on_delete=models.PROTECT)
    quantidadeUsada = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.peca.quantidade < self.quantidadeUsada:
            raise ValueError("Estoque insuficiente para a peça selecionada.")
        self.peca.quantidade -= self.quantidadeUsada
        self.peca.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantidadeUsada}x {self.peca.nome} na OS {self.ordemServico.pk}"

class OrdemServico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='ordens_servico')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='ordens_servico')
    pecas = models.ManyToManyField(Peca, blank=True, related_name='ordens_servico', through='PecaUsada')
    Kilometragem = models.PositiveIntegerField()
    dataEntrada = models.DateField(auto_now_add=True)
    dataSaida = models.DateField(blank=True, null=True)
    feito = models.BooleanField(default=False)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.veiculo} ({self.servico})"
