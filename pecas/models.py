from django.db import models

class Peca(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valorUN = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
