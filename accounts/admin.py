from django.contrib import admin
from accounts.models import Endereco

# Register your models here.
class EndereAdmin(admin.ModelAdmin):
    list_display = ('usuario','celular', 'rua', 'numero', 'complemento', 'cidade', 'estado', 'cep', 'principal')
    search_fields = ('usuario', 'cidade', 'cep', 'estado', 'rua')

admin.site.register(Endereco, EndereAdmin)