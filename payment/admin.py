from django.contrib import admin
from .models import Pedido
# Register your models here.

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'itens', 'total', 'status', 'data_pedido')
    search_fields = ('usuario', 'status', 'data_pedido',)

admin.site.register(Pedido, PedidoAdmin)