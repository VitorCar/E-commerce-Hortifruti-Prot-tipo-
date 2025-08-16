from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import json

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('aprovado', 'Aprovado'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    itens = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)

    def get_itens(self):
        """
        Retorna os itens do pedido em formato de lista de dicts
        [{id: int, nome: str, quantidade: int}]
        """
        try:
            data = json.loads(self.itens)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return list(data.values())
        except Exception:
            pass
        return []