from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class MedidaCobrar(models.Model):
    medida = models.CharField(max_length=100)
    
    def __str__(self):
        return self.medida


class Produto(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    medida = models.ForeignKey(MedidaCobrar, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to='produtos/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Promocao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    new_value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.produto.name} em promoção por R${self.new_value:.2f}'