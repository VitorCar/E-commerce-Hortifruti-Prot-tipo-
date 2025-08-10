from django.db import models
from django.contrib.auth.models import User

class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enderecos')
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)
    celular = models.CharField(max_length=11)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.rua} - {self.numero} - {self.cidade} - {self.celular}'
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'