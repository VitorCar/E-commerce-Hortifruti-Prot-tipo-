from django.contrib import admin

# Register your models here.
from core.models import Category, Produto, MedidaCobrar, Promocao

class ProdAdmin(admin.ModelAdmin):
    list_display = ('name', 'medida', 'value', 'stock' ,'category', 'description', 'image')
    search_fields = ('name', 'category', 'value',)


class CategAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MedidAdmin(admin.ModelAdmin):
    list_display = ('medida',)
    search_fields = ('medida',)

class PromAdmin(admin.ModelAdmin):
    list_display = ( 'produto', 'new_value')
    search_fields = ('produto',)

admin.site.register(Category, CategAdmin)
admin.site.register(Produto, ProdAdmin)
admin.site.register(MedidaCobrar, MedidAdmin)
admin.site.register(Promocao, PromAdmin)

