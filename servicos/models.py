from django.db import models

class Servico(models.Model):
    descricao = models.CharField(max_length=100)
    tempo = models.DurationField()  # Tempo estimado para o serviço
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço da mão de obra

    def __str__(self):
        return self.descricao
