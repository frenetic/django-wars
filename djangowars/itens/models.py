from django.db import models


class Arma(models.Model):
    poder = models.PositiveSmallIntegerField()
    compra = models.FloatField() # valor de compra
    venda = models.FloatField() # valor de venda
    secreta = models.BooleanField(default=False) #se a arma eh secreta ou disponivel na loja
    
    imagem = models.ImageField(upload_to="armas") #imagem do item


class Armadura(models.Model):
    poder = models.PositiveSmallIntegerField()
    compra = models.FloatField() # valor de compra
    venda = models.FloatField() # valor de venda
    secreta = models.BooleanField(default=False) #se a armadura eh secreta ou disponivel na loja
    
    imagem = models.ImageField(upload_to="armaduras") #imagem do item